import json
import requests

with open("data/events.jsonl", "r") as f:

    for line in f:

        event = json.loads(line)

        response = requests.post(
            "http://127.0.0.1:8000/events/ingest",
            json=event
        )

        print(response.json())