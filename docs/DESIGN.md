# System Design Document

## Overview

The AI Store Intelligence System converts CCTV footage into actionable retail analytics through computer vision and event-driven architecture.

## High-Level Architecture

Video Source
→ Detection Layer
→ Tracking Layer
→ Analytics Layer
→ API Layer
→ Dashboard Layer

## Detection Layer

YOLOv8 is used to detect people in each frame. The model provides real-time inference and high detection accuracy suitable for retail environments.

## Tracking Layer

ByteTrack assigns persistent IDs to detected customers across consecutive frames. This enables customer journey analysis and conversion tracking.

## Zone Analytics Layer

The store layout is divided into predefined zones:

* ENTRANCE
* LEFT_SHELF
* CENTER_SHELF
* RIGHT_SHELF
* BILLING

Customer positions are mapped to these zones using coordinate-based logic.

## Event Processing Layer

The system generates:

* ENTRY
* ZONE_ENTER
* PURCHASE

These events are stored in SQLite and used by analytics APIs.

## Analytics Layer

The analytics engine computes:

* Customer Journeys
* Conversion Funnel
* Heatmaps
* Anomalies
* Store Metrics

## API Layer

FastAPI exposes REST APIs for retrieving analytics and business insights.

## Dashboard Layer

Streamlit provides a visual dashboard showing KPIs, customer journeys, heatmaps, conversion rates, and anomaly alerts.

## Scalability Considerations

For large-scale deployment:

* SQLite can be replaced by PostgreSQL
* Message queues can be introduced
* Multi-camera processing can be added
* Cloud deployment can be supported

## AI-Assisted Decisions


During development, AI tools such as ChatGPT were used to evaluate design options and accelerate implementation.

### Decision 1: Detection Model Selection

AI suggested YOLOv8, Faster R-CNN, and RT-DETR.

After evaluating the trade-offs, YOLOv8 was selected because it provides real-time performance and simple integration with the tracking pipeline.

### Decision 2: Tracking Approach

AI suggested both DeepSORT and ByteTrack.

ByteTrack was selected because it provided stable tracking IDs with less configuration complexity and worked well for retail CCTV footage.

### Decision 3: Zone Classification

AI suggested both VLM-based classification and rule-based zone mapping.

Rule-based zone mapping was selected because store layouts are predefined and coordinate-based mapping is faster and more reliable than introducing another AI model.
