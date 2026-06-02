from collections import defaultdict

def calculate_dwell(events):

    dwell = defaultdict(int)

    for event in events:

        visitor = event["visitor_id"]

        dwell[visitor] += 1

    return dict(dwell)