from ultralytics import YOLO
import cv2

from zones import get_zone
from emit import emit_event

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("data/videos/store.mp4")

visitor_zones = {}

while True:

    ret, frame = video.read()

    if not ret:
        print("Video Finished")
        break

    results = model.track(
        frame,
        persist=True,
        classes=[0],
        verbose=False
    )

    boxes = results[0].boxes

    if boxes.id is not None:

        ids = boxes.id.int().cpu().tolist()

        coords = boxes.xyxy.cpu().tolist()

        for track_id, box in zip(ids, coords):

            x1, y1, x2, y2 = map(int, box)

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            current_zone = get_zone(center_x, center_y)

            if track_id not in visitor_zones:

                visitor_zones[track_id] = current_zone

                emit_event(
                    f"VIS_{track_id}",
                    "ZONE_ENTER",
                    current_zone
                )

            elif visitor_zones[track_id] != current_zone:

                emit_event(
                    f"VIS_{track_id}",
                    "ZONE_EXIT",
                    visitor_zones[track_id]
                )

                emit_event(
                    f"VIS_{track_id}",
                    "ZONE_ENTER",
                    current_zone
                )

                visitor_zones[track_id] = current_zone

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"ID:{track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    cv2.line(frame, (640, 0), (640, 1080), (255, 0, 0), 2)
    cv2.line(frame, (1280, 0), (1280, 1080), (255, 0, 0), 2)

    display_frame = cv2.resize(frame, (1280, 720))

    cv2.imshow("STORE INTELLIGENCE", display_frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()