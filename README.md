# AI Store Intelligence System

## Problem Statement

Retail stores generate large amounts of CCTV footage, but extracting actionable business insights manually is difficult and time-consuming.

This project converts CCTV video streams into actionable retail analytics using Computer Vision and AI. The system detects customers, tracks movement across store zones, generates customer journeys, calculates conversion funnels, detects anomalies, and provides business insights through APIs and dashboards.

---

## Solution Overview

The AI Store Intelligence System processes CCTV footage using YOLOv8 and ByteTrack to generate structured retail events.

These events are stored in a database and used to compute:

* Customer Journeys
* Conversion Funnels
* Heatmaps
* Purchase Analytics
* Staff Detection
* Anomaly Detection
* Store-Level Metrics

The results are exposed through FastAPI endpoints and visualized in a Streamlit dashboard.

---

## Features

### Computer Vision

* Customer Detection using YOLOv8
* Multi-Object Tracking using ByteTrack
* Zone Classification
* Entry Detection
* Re-Entry Detection
* Purchase Detection
* Staff Detection

### Analytics

* Customer Journey Analytics
* Conversion Funnel Analytics
* Heatmap Analytics
* Anomaly Detection
* Store-Level Metrics

### Backend

* FastAPI REST APIs
* SQLite Database
* Event Ingestion Pipeline
* Structured Logging
* Graceful Error Handling

### Dashboard

* Real-Time KPI Dashboard
* Visitor Metrics
* Event Analytics
* Conversion Analytics
* Journey Analytics
* Zone Analytics
* Staff Analytics

---

## Technology Stack

### Computer Vision

* YOLOv8
* ByteTrack
* OpenCV

### Backend

* FastAPI
* Pydantic
* SQLite

### Frontend

* Streamlit

### Testing

* PyTest

---

## System Architecture

CCTV Video

↓

YOLOv8 Person Detection

↓

ByteTrack Tracking

↓

Zone Classification

↓

Event Generation

↓

FastAPI Event Ingestion

↓

SQLite Database

↓

Analytics APIs

↓

Streamlit Dashboard

---

## Event Schema

The system generates the following events:

* ENTRY
* EXIT
* REENTRY
* ZONE_ENTER
* PURCHASE
* STAFF_DETECTED

These events are stored in the database and used for analytics computation.

---

## Detection Pipeline

### Input

The detection pipeline processes CCTV footage located at:

data/videos/store.mp4

### Detection Model

YOLOv8 is used for person detection.

### Tracking Model

ByteTrack is used to assign persistent visitor IDs.

### Run Detection Pipeline

python pipeline/detect.py

### Output

The pipeline generates structured retail events and sends them to:

POST /events/ingest

Examples:

* ENTRY
* ZONE_ENTER
* PURCHASE
* STAFF_DETECTED
* EXIT
* REENTRY

---

## Event Flow

Detection Pipeline

↓

POST /events/ingest

↓

SQLite Database (store.db)

↓

Analytics APIs

↓

Dashboard

---

## APIs

### Core APIs

* POST /events/ingest
* GET /events
* GET /metrics
* GET /health
* GET /funnel
* GET /conversion
* GET /journey

### Store-Specific APIs

* GET /stores/{store_id}/metrics
* GET /stores/{store_id}/funnel
* GET /stores/{store_id}/journey
* GET /stores/{store_id}/heatmap
* GET /stores/{store_id}/anomalies

### Utility APIs

* DELETE /reset

---

## Running the Complete System

### Terminal 1 – Backend

uvicorn app.main:app --reload

### Terminal 2 – Detection Pipeline

python pipeline/detect.py

### Terminal 3 – Dashboard

streamlit run dashboard/app.py

---

## Dashboard

Open:

http://localhost:8501

Dashboard Features:

* Visitor Count
* Event Count
* Conversion Rate
* Health Status
* Staff Count
* Conversion Funnel
* Zone Analytics
* Customer Journey Analytics
* Heatmap Analytics

---

## API Documentation

Open Swagger UI:

http://127.0.0.1:8000/docs

Verify:

* POST /events/ingest
* GET /metrics
* GET /funnel
* GET /journey
* GET /stores/{store_id}/heatmap
* GET /stores/{store_id}/anomalies

---

## Testing

Run all tests:

pytest tests

Expected Result:

3 passed

Test Coverage:

* Pipeline Validation
* Metrics Validation
* Anomaly Validation

---

## Production Readiness

Implemented:

* Structured Logging
* Graceful Error Handling (HTTP 503)
* Event Deduplication
* API Documentation
* Docker Configuration
* Unit Testing

---

## Results

Successfully implemented:

* Customer Detection
* Customer Tracking
* Customer Journey Generation
* Purchase Detection
* Staff Detection
* Conversion Funnel Analytics
* Heatmap Analytics
* Anomaly Detection
* Real-Time Dashboard Analytics

---

## Future Enhancements

* Multi-Camera Support
* Cross-Camera Re-Identification
* PostgreSQL Backend
* Cloud Deployment
* Kafka-Based Event Streaming
* Real-Time Multi-Store Analytics

---

## Author

AI Store Intelligence System

Built for Retail Analytics using Computer Vision, FastAPI, and Streamlit.


