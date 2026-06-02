import json

with open("data/store_layout.json") as f:
    ZONES = json.load(f)

def get_zone(x, y):

    for zone_name, coords in ZONES.items():

        x1, y1, x2, y2 = coords

        if x1 <= x <= x2 and y1 <= y <= y2:
            return zone_name

    return None