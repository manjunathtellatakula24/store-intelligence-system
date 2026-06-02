import json
import uuid
from datetime import datetime


def emit_event(
    visitor_id,
    event_type,
    zone_id,
    store_id="STORE_BLR_002",
    camera_id="CAM_MAIN_01"
):

    event = {

        "event_id": str(uuid.uuid4()),

        "store_id": store_id,

        "camera_id": camera_id,

        "visitor_id": visitor_id,

        "event_type": event_type,

        "timestamp": datetime.utcnow().isoformat(),

        "zone_id": zone_id,

        "dwell_ms": 0,

        "is_staff": False,

        "confidence": 0.95,

        "metadata": {
            "queue_depth": None,
            "sku_zone": zone_id,
            "session_seq": 1
        }
    }

    with open(
        "data/events.jsonl",
        "a"
    ) as f:

        f.write(
            json.dumps(event) + "\n"
        )

    print(event)

    return event