import time
import uuid
from datetime import datetime
import cv2
import requests
import supervision as sv
from ultralytics import YOLO

from zones import get_zone

print("STORE INTELLIGENCE STARTED")

model = YOLO("yolov8n.pt")

tracker = sv.ByteTrack()
video = cv2.VideoCapture("data/videos/store.mp4")

visitor_zones = {}
visitor_last_change = {}
known_visitors = set()
visitor_last_seen = {}
reentry_cooldown = {}
last_dwell_emit = {}  # Initialized missing dictionary to prevent future KeyErrors

track_counts = {}
billing_start_time = {}
purchased_visitors = set()
staff_detected = set()
session_sequence = {}

COOLDOWN_SECONDS = 3
VISITOR_TIMEOUT = 5
EXIT_TIMEOUT = 10

while True:

    ret, frame = video.read()

    if not ret:
        break

    result = model(frame, classes=[0], verbose=False)[0]

    detections = sv.Detections.from_ultralytics(result)
    detections = detections[detections.confidence > 0.65]

    detections = tracker.update_with_detections(detections)

    # Ensure tracker ids exist and lengths match before iterating
    if detections.tracker_id is not None and len(detections.tracker_id) > 0:
        for box, track_id in zip(detections.xyxy, detections.tracker_id):
            x1, y1, x2, y2 = box

            # ensure coordinates are numeric and convert to ints
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
            width = x2 - x1
            height = y2 - y1

            if width < 40 or height < 100:
                continue

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            zone = get_zone(center_x, center_y)
            visitor_id = f"VIS_{track_id}"
            current_time = time.time()

            # ENTRY ONLY ONCE
            if visitor_id not in known_visitors:

                event_type = "ENTRY"

                if (
                    visitor_id in visitor_last_seen
                    and current_time - visitor_last_seen[visitor_id] < 300
                ):

                    last_reentry = reentry_cooldown.get(visitor_id, 0)

                    if current_time - last_reentry > 30:
                        event_type = "REENTRY"
                        reentry_cooldown[visitor_id] = current_time

                known_visitors.add(visitor_id)

                session_sequence[visitor_id] = (
                    session_sequence.get(visitor_id, 0) + 1
                )

                entry_event = {
                    "event_id": str(uuid.uuid4()),
                    "store_id": "STORE_BLR_002",
                    "camera_id": "CAM_MAIN_01",
                    "visitor_id": visitor_id,
                    "event_type": event_type,
                    "timestamp": datetime.utcnow().isoformat(),
                    "zone_id": zone,
                    "dwell_ms": 0,
                    "is_staff": False,
                    "confidence": 0.95,
                    "metadata": {
                        "queue_depth": None,
                        "session_seq": session_sequence[visitor_id],
                        "sku_zone": zone,
                    },
                }

                requests.post(
                    "http://127.0.0.1:8000/events/ingest", json=entry_event
                )

                print(event_type, visitor_id, zone)

            elif visitor_zones.get(visitor_id) != zone:
                # FIXED: Only process exit event if visitor has a previous registered zone
                if visitor_id in visitor_zones:
                    exit_zone_event = {
                        "event_id": str(uuid.uuid4()),
                        "store_id": "STORE_BLR_002",
                        "camera_id": "CAM_MAIN_01",
                        "visitor_id": visitor_id,
                        "event_type": "ZONE_EXIT",
                        "timestamp": datetime.utcnow().isoformat(),
                        "zone_id": visitor_zones[visitor_id],
                        "dwell_ms": 0,
                        "is_staff": False,
                        "confidence": 0.95,
                        "metadata": {
                            "queue_depth": None,
                            "session_seq": session_sequence[visitor_id],
                            "sku_zone": visitor_zones[visitor_id],
                        },
                    }

                    requests.post(
                        "http://127.0.0.1:8000/events/ingest",
                        json=exit_zone_event,
                    )

                last_time = visitor_last_change.get(visitor_id, current_time)
                if (current_time - last_time) >= COOLDOWN_SECONDS:
                    dwell_time = current_time - last_time
                    visitor_zones[visitor_id] = zone
                    visitor_last_change[visitor_id] = current_time
                    
                    if dwell_time > 30:
                        last_emit = last_dwell_emit.get(visitor_id, 0)
                        if current_time - last_emit > 30:
                            dwell_event = {
                                "event_id": str(uuid.uuid4()),
                                "store_id": "STORE_BLR_002",
                                "camera_id": "CAM_MAIN_01",
                                "visitor_id": visitor_id,
                                "event_type": "ZONE_DWELL",
                                "timestamp": datetime.utcnow().isoformat(),
                                "zone_id": zone,
                                "dwell_ms": int(dwell_time * 1000),
                                "is_staff": False,
                                "confidence": 0.95,
                                "metadata": {
                                    "queue_depth": None,
                                    "session_seq": session_sequence[
                                        visitor_id
                                    ],
                                    "sku_zone": zone,
                                },
                            }

                            requests.post(
                                "http://127.0.0.1:8000/events/ingest",
                                json=dwell_event,
                            )

                            last_dwell_emit[visitor_id] = current_time

                    zone_event = {
                        "event_id": str(uuid.uuid4()),
                        "store_id": "STORE_BLR_002",
                        "camera_id": "CAM_MAIN_01",
                        "visitor_id": visitor_id,
                        "event_type": "ZONE_ENTER",
                        "timestamp": datetime.utcnow().isoformat(),
                        "zone_id": zone,
                        "dwell_ms": 0,
                        "is_staff": False,
                        "confidence": 0.95,
                        "metadata": {
                            "queue_depth": None,
                            "session_seq": session_sequence[visitor_id],
                            "sku_zone": zone,
                        },
                    }

                    requests.post(
                        "http://127.0.0.1:8000/events/ingest", json=zone_event
                    )
                    print("ZONE_ENTER:", visitor_id, zone)

            cv2.rectangle(
                frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2
            )
            cv2.putText(
                frame,
                f"ID {track_id}",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            if zone:
                cv2.putText(
                    frame,
                    str(zone),
                    (int(x1), int(y2) + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 0),
                    2,
                )

            # PURCHASE DETECTION
            if zone == "BILLING":
                if visitor_id not in billing_start_time:
                    billing_start_time[visitor_id] = current_time
                
                stay_time = current_time - billing_start_time[visitor_id]

                # STAFF DETECTION (long dwell indicates staff)
                if stay_time >= 20 and visitor_id not in staff_detected:
                    staff_detected.add(visitor_id)
                    staff_event = {
                        "event_id": str(uuid.uuid4()),
                        "store_id": "STORE_BLR_002",
                        "camera_id": "CAM_MAIN_01",
                        "visitor_id": visitor_id,
                        "event_type": "STAFF_DETECTED",
                        "timestamp": datetime.utcnow().isoformat(),
                        "zone_id": "BILLING",
                        "dwell_ms": int(stay_time * 1000),
                        "is_staff": True,
                        "confidence": 0.95,
                        "metadata": {
                            "queue_depth": None,
                            "session_seq": session_sequence.get(visitor_id, 1),
                            "sku_zone": "BILLING",
                        },
                    }

                    requests.post(
                        "http://127.0.0.1:8000/events/ingest", json=staff_event
                    )
                    print("STAFF_DETECTED:", visitor_id)

                # PURCHASE DETECTION
                if stay_time >= 5 and visitor_id not in purchased_visitors:
                    purchased_visitors.add(visitor_id)
                    purchase_event = {
                        "event_id": str(uuid.uuid4()),
                        "store_id": "STORE_BLR_002",
                        "camera_id": "CAM_MAIN_01",
                        "visitor_id": visitor_id,
                        "event_type": "PURCHASE",
                        "timestamp": datetime.utcnow().isoformat(),
                        "zone_id": "BILLING",
                        "dwell_ms": int(stay_time * 1000),
                        "is_staff": False,
                        "confidence": 0.95,
                        "metadata": {
                            "queue_depth": None,
                            "session_seq": session_sequence.get(visitor_id, 1),
                            "sku_zone": "BILLING",
                        },
                    }

                    requests.post(
                        "http://127.0.0.1:8000/events/ingest",
                        json=purchase_event,
                    )
                    print("PURCHASE:", visitor_id)
            else:
                if visitor_id in billing_start_time:
                    del billing_start_time[visitor_id]

    active_visitors = set()

    if detections.tracker_id is not None:
        for track_id in detections.tracker_id:
            active_visitors.add(f"VIS_{track_id}")

    for visitor in list(known_visitors):

        if visitor not in active_visitors:

            if visitor not in visitor_last_seen:
                visitor_last_seen[visitor] = time.time()

            elif time.time() - visitor_last_seen[visitor] > EXIT_TIMEOUT:

                exit_event = {
                    "event_id": str(uuid.uuid4()),
                    "store_id": "STORE_BLR_002",
                    "camera_id": "CAM_MAIN_01",
                    "visitor_id": visitor,
                    "event_type": "EXIT",
                    "timestamp": datetime.utcnow().isoformat(),
                    "zone_id": None,
                    "dwell_ms": 0,
                    "is_staff": False,
                    "confidence": 0.95,
                    "metadata": {
                    "queue_depth": None,
                    "session_seq": session_sequence.get(visitor, 1),
                    "sku_zone": None
                }
                }

                requests.post(
                    "http://127.0.0.1:8000/events/ingest", json=exit_event
                )

                known_visitors.remove(visitor)
                if visitor in visitor_zones:
                    del visitor_zones[visitor]

    cv2.imshow("STORE INTELLIGENCE", frame)

    key = cv2.waitKey(30)

    if key == ord("q") or key == 27:
        break

video.release()
cv2.destroyAllWindows()