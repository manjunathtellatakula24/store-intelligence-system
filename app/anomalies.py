def detect_anomalies(events):

    anomalies = []

    billing_count = len([
        e for e in events
        if e.get("zone_id") == "BILLING"
    ])

    if billing_count > 20:

        anomalies.append({

            "type":
            "QUEUE_SPIKE",

            "severity":
            "WARN",

            "suggested_action":
            "Open additional billing counter"
        })

    conversion_events = len([
        e for e in events
        if e.get("event_type") == "PURCHASE"
    ])

    if conversion_events == 0:

        anomalies.append({

            "type":
            "CONVERSION_DROP",

            "severity":
            "INFO",

            "suggested_action":
            "Review store conversion performance"
        })

    return anomalies