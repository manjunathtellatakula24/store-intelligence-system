def generate_heatmap(events):

    zone_stats = {}

    for event in events:

        zone = event.get("zone_id")

        if not zone:
            continue

        zone_stats[zone] = (
            zone_stats.get(zone, 0) + 1
        )

    max_visits = (
        max(zone_stats.values())
        if zone_stats else 1
    )

    result = []

    for zone, count in zone_stats.items():

        result.append({

            "zone": zone,

            "visits": count,

            "normalized": round(
                (count / max_visits) * 100,
                2
            ),

            "data_confidence":
            "HIGH"
            if count >= 20
            else "LOW"
        })

    return result