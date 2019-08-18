# -*- coding: utf-8 -*-
import datetime as dt
import json
import math
import os

# import requests
from botocore.vendored import requests

api_token = os.environ["AIRTABLE_API_TOKEN"]
base_id = os.environ["AIRTABLE_PLANTS_BASE_ID"]


# noinspection PyUnusedLocal
def check_water_status(event, context):
    """AWS Lambda function handler to check plant status.
    """
    print(os.environ.keys())  # temp

    url = f"https://api.airtable.com/v0/{base_id}/plants"
    r = requests.get(url, headers={"Authorization": f"Bearer {api_token}"})

    return {
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(get_plant_info(r.json()["records"])),
        "isBase64Encoded": False,
        "statusCode": 200,
    }


def get_plant_info(records):
    """Return a list, sorted by last watered, of my plants with some metadata.
    """
    plant_info = []

    for rec in records:
        fields = rec["fields"]

        last_watered = dt.datetime.fromisoformat(fields["lastwatereddate"][:-1])
        seconds_since = int(abs((dt.datetime.now() - last_watered).total_seconds()))
        days_since = math.floor(seconds_since // 3600 / 24)

        message = f"Last watered {'today' if days_since == 0 else str(days_since) + ' days ago'}."

        plant_info.append(
            {
                "id": rec["id"],
                "plantname": fields["plantname"],
                "seconds_since": seconds_since,
                "message": message,
                "needs_water": days_since > fields["waterinterval"],
                "needs_water_soon": days_since > fields["waterinterval"] - 2,
            }
        )

    return sorted(plant_info, reverse=True, key=lambda x: x["seconds_since"])
