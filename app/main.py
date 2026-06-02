from app.anomalies import detect_anomalies
from app.heatmap import generate_heatmap
from fastapi import FastAPI, HTTPException
from app.models import Event
from app.database import conn, cursor
from app.journey import customer_journey
import json
import logging

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@app.get("/")
def home():
    return {
        "message": "Store Intelligence Running"
    }


@app.post("/events/ingest")
def ingest(event: Event):

    try:
        logger.info(
    f"store={event.store_id} "
    f"visitor={event.visitor_id} "
    f"event={event.event_type}"
    )
        cursor.execute(
            """
            INSERT OR IGNORE INTO events
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                event.event_id,
                event.store_id,
                event.camera_id,
                event.visitor_id,
                event.event_type,
                event.timestamp,
                event.zone_id,
                event.dwell_ms,
                int(event.is_staff),
                event.confidence,
                json.dumps(event.metadata)
            )
        )

        conn.commit()

        return {
            "status": "success",
            "event_id": event.event_id
        }

    except Exception as e:

        logger.error(
        f"Database error: {str(e)}"
    )

    raise HTTPException(
        status_code=503,
        detail="Database unavailable"
    )


@app.get("/events")
def get_events():

    rows = cursor.execute(
        "SELECT * FROM events"
    ).fetchall()

    events = []

    for row in rows:

        events.append({

            "event_id": row[0],
            "store_id": row[1],
            "camera_id": row[2],
            "visitor_id": row[3],
            "event_type": row[4],
            "timestamp": row[5],
            "zone_id": row[6],
            "dwell_ms": row[7],
            "is_staff": bool(row[8]),
            "confidence": row[9],
            "metadata": json.loads(row[10])
            if row[10]
            else {}
        })

    return events


@app.get("/metrics")
def metrics():

    events = get_events()

    visitors = set()

    for event in events:

        if not event["is_staff"]:

            visitors.add(
                event["visitor_id"]
            )
    staff_count = len(set([
        e["visitor_id"]
        for e in events
        if e["is_staff"]
    ]))


    return {

        "total_visitors":
        len(visitors),

        "total_events":
        len(events),

        "staff_count":
        staff_count
    }


@app.get("/health")
def health():

    events = get_events()

    return {

        "status": "healthy",

        "events_ingested":
        len(events)
    }


@app.get("/funnel")
def funnel():

    events = get_events()

    entered = len([
        e for e in events
        if e["event_type"] == "ENTRY"
    ])

    zone_visits = len([
        e for e in events
        if e["event_type"] == "ZONE_ENTER"
    ])

    billing_queue = len([
        e for e in events
        if e["event_type"] == "BILLING_QUEUE_JOIN"
    ])

    purchased = len([
        e for e in events
        if e["event_type"] == "PURCHASE"
    ])

    conversion_rate = 0

    if entered > 0:

        conversion_rate = round(
            (purchased / entered) * 100,
            2
        )

    return {

        "entered": entered,
        "zone_visits": zone_visits,
        "billing_queue": billing_queue,
        "purchased": purchased,
        "conversion_rate": conversion_rate
    }
@app.get("/conversion")
def conversion():

    events = get_events()

    entered = len([
        e for e in events
        if e["event_type"] == "ENTRY"
    ])

    purchased = len([
        e for e in events
        if e["event_type"] == "PURCHASE"
    ])

    rate = 0

    if entered > 0:
        rate = round(
            (purchased / entered) * 100,
            2
        )

    return {
        "entries": entered,
        "purchases": purchased,
        "conversion_rate": rate
    }

@app.get("/journey")
def journey():

    events = get_events()

    return customer_journey(events)

    events = get_events()

    entered = len([
        e for e in events
        if e["event_type"] == "ENTRY"
    ])

    purchased = len([
        e for e in events
        if e["event_type"] == "PURCHASE"
    ])

    rate = 0

    if entered > 0:

        rate = round(
            (purchased / entered) * 100,
            2
        )

    return {

        "entries": entered,
        "purchases": purchased,
        "conversion_rate": rate
    }
@app.get("/stores/{store_id}/metrics")
def store_metrics(store_id: str):

    events = get_events()

    store_events = [
        e for e in events
        if e["store_id"] == store_id
    ]

    visitors = set()

    for event in store_events:

        if not event["is_staff"]:
            visitors.add(event["visitor_id"])

    return {
        "store_id": store_id,
        "total_visitors": len(visitors),
        "total_events": len(store_events)
    }
@app.get("/stores/{store_id}/heatmap")
def heatmap(store_id: str):

    events = get_events()

    store_events = [
        e for e in events
        if e["store_id"] == store_id
    ]

    return generate_heatmap(
        store_events
    )
@app.get("/stores/{store_id}/anomalies")
def anomalies(store_id: str):

    events = get_events()

    store_events = [
        e for e in events
        if e["store_id"] == store_id
    ]

    return detect_anomalies(
        store_events
    )

@app.delete("/reset")
def reset():

    cursor.execute(
        "DELETE FROM events"
    )

    conn.commit()

    return {
        "status": "database cleared"
    }