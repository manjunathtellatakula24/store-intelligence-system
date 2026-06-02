def detect_anomalies(events):

    zone_counts = {}

    for event in events:

        zone = event["zone"]

        zone_counts[zone] = zone_counts.get(zone, 0) + 1

    alerts = []

    for zone, count in zone_counts.items():

        if count >= 10:

            alerts.append(
                f"Crowd detected in {zone}"
            )

    if not alerts:

        alerts.append(
            "No anomalies detected"
        )

    return alerts