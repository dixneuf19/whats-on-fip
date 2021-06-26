import os
from typing import List

import requests
from dotenv import load_dotenv
from loguru import logger

from whatsonfip.models import Track

load_dotenv()

RADIO_MEUH_API_URL = os.getenv(
    "RADIO_MEUH_API_URL", "https://www.radiomeuh.com/player/rtdata/tracks.json"
)


def get_current_song() -> Track:
    r = requests.get(url=RADIO_MEUH_API_URL)
    song = r.json()[0]
    logger.debug(song)

    song["title"] = song["titre"]
    # song["album"] = song["album"]
    # song["artist"] = song["artist"]

    song["external_urls"] = {}
    if song["url"] != "":
        song["external_urls"]["spotify"] = song["url"]

    song["cover_url"] = song["imgSrc"]

    return Track(**song)
