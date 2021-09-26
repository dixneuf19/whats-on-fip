import os

import requests
from dotenv import load_dotenv

from whatsonfip.models import Track

load_dotenv()

RADIO_MEUH_API_URL = os.getenv(
    "RADIO_MEUH_API_URL", "https://www.radiomeuh.com/player/rtdata/tracks.json"
)


def get_current_song() -> Track:
    r = requests.get(url=RADIO_MEUH_API_URL)
    song = r.json()[0]

    song = {
        **song,
        "title": song["titre"],
        "external_urls": {"spotify": song["url"]} if song["url"] != "" else {},
        "cover_url": song["imgSrc"],
    }

    return Track(**song)
