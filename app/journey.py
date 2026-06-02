from collections import defaultdict

def customer_journey(events):

    journeys = defaultdict(list)

    for event in events:

        visitor = event.get("visitor_id")
        zone = event.get("zone_id")

        if not visitor or not zone:
            continue

        if zone not in journeys[visitor]:
            journeys[visitor].append(zone)

    return dict(journeys)