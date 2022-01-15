import os

import requests
from dotenv import load_dotenv

from whats_on_fip.models import Track

load_dotenv()

UNOFFICIAL_API_URL = os.getenv(
    "UNOFFICIAL_API_URL", "https://www.fip.fr/latest/api/graphql"
)
UNOFFICIAL_API_OPERATION_NOW = os.getenv(
    "UNOFFICIAL_API_OPERATION_NOW",
    "?operationName=Now&variables=%7B%22bannerPreset%22%3A%22266x266%22%2C%22stationId%22%3A7%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2295ed3dd1212114e94d459439bd60390b4d6f9e37b38baf8fd9653328ceb3b86b%22%7D%7D",  # noqa: E501
)


def get_now_unofficial() -> Track:
    r = requests.get(url=UNOFFICIAL_API_URL + UNOFFICIAL_API_OPERATION_NOW)
    r.raise_for_status()
    song = r.json()["data"]["now"]["song"]

    song["artist"] = song["interpreters"][0] if len(song["interpreters"]) > 0 else ""

    song["cover_url"] = song["cover"]

    song["external_urls"] = {}
    for key, value in song["external_links"].items():
        if not (key.startswith("__") or value is None):
            song["external_urls"][key] = value["link"]

    # Special case uncountered once : album is none
    song["album"] = "" if song["album"] is None else song["album"]

    return Track(**song)
