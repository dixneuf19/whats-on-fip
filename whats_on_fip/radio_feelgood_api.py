import os
from time import time

import requests

from whats_on_fip.models import Track
from whats_on_fip.radio import Radio
from whats_on_fip.spotify_api import get_spotify_url


class RadioFeelGood(Radio):
    def __init__(self) -> None:
        self.url = os.getenv(
            "RADIO_FEELGOOD_URL", "https://www.radiofg.com/api/TitleDiffusions"
        )
        self.common_params = {
            "size": "1",  # Select only the last song
            "radioStreamId": "2174546520932614607",
        }
        self.cover_url = "https://images.lesindesradios.fr/fit-in/300x2000/filters:quality(100)/radios/radiofg/radiostream/5gWkrl9VKE/vignette_awN7JwWOid.jpeg"  # noqa:E501

    def get_current_track(self) -> Track:
        # 1. Generate current timestamp + 000 (reverse-engineered)
        current_ts = f"{int(time())}000"

        # 2. Query API for this timestamp
        res = requests.get(self.url, params={**self.common_params, "date": current_ts})
        res.raise_for_status()

        song = res.json()[0]["title"]

        # 3. Adapt for our format

        external_urls = {}
        if "spotifyId" in song and song["spotifyId"] is not None:
            external_urls["spotify"] = get_spotify_url(song["spotifyId"])
        song = {
            **song,
            "external_urls": external_urls,
            # "cover_url"  # Hard to compute for now, serve generic radio FG Thumbnail
            "cover_url": self.cover_url,
        }

        return Track(**song)
