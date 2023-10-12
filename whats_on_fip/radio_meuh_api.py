import os

import requests

from whats_on_fip.models import Track
from whats_on_fip.radio import Radio


class RadioMeuh(Radio):
    def __init__(self) -> None:
        self.url = os.getenv(
            "RADIO_MEUH_API_URL", "https://www.radiomeuh.com/player/rtdata/tracks.json"
        )

    def get_current_track(self) -> Track:
        r = requests.get(self.url)
        r.raise_for_status()
        song = r.json()[0]

        song = {
            **song,
            "title": song["titre"],
            "external_urls": {"spotify": song["url"]} if song["url"] != "" else {},
            "cover_url": song["imgSrc"],
        }

        return Track(**song)
