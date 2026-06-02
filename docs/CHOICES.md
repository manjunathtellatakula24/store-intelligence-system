

## Choice 1: Detection Model Selection

### Options Considered

* YOLOv8
* RT-DETR
* Faster R-CNN

### What AI Suggested

AI suggested YOLOv8, RT-DETR, and Faster R-CNN as possible person detection models.

### What I Chose

YOLOv8

### Why

YOLOv8 provided the best balance of detection accuracy, inference speed, and ease of integration. Since the project required real-time retail analytics, low latency was important. Faster R-CNN provided good accuracy but was slower, while RT-DETR required more tuning for the available dataset.

---

## Choice 2: Event Schema Design

### Options Considered

* Raw frame-level detections
* Bounding-box storage
* Event-driven schema

### What AI Suggested

AI suggested storing frame-level detections and deriving analytics later.

### What I Chose

Event-driven schema using ENTRY, ZONE_ENTER, PURCHASE, STAFF_DETECTED, and REENTRY events.

### Why

Business analytics are easier to compute from events than from raw detections. Event-driven processing reduces storage requirements and simplifies conversion funnels, customer journeys, anomaly detection, and heatmap generation.

---

## Choice 3: API Architecture Decision

### Options Considered

* Flask REST API
* FastAPI
* Monolithic analytics script

### What AI Suggested

AI suggested both Flask and FastAPI implementations.

### What I Chose

FastAPI with an event ingestion architecture.

### Why

FastAPI provides automatic API documentation, request validation through Pydantic models, and a clean structure for analytics endpoints. Separating detection from analytics through event ingestion improves maintainability and scalability.
