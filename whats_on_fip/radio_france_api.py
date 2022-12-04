import os
from typing import Any, Dict, List

import requests
from loguru import logger

from whats_on_fip.models import Station, Track
from whats_on_fip.radio import Radio

API_TOKEN = os.getenv("RADIO_FRANCE_API_TOKEN")

RADIO_FRANCE_API_HOST = os.getenv(
    "RADIO_FRANCE_API_HOST", "https://openapi.radiofrance.fr/v1/graphql"
)

RADIO_FRANCE_API_URL = f"{RADIO_FRANCE_API_HOST}?x-token={API_TOKEN}"


class LiveUnavailableException(Exception):
    pass


class RadioFIP(Radio):
    def __init__(self) -> None:
        self.station = "FIP"
        self.url = RADIO_FRANCE_API_URL
        self.unnoficial_api = os.getenv(
            "UNOFFICIAL_API_URL", "https://www.fip.fr/latest/api/graphql"
        )
        self.unnoficial_api_operation_now = os.getenv(
            "UNOFFICIAL_API_OPERATION_NOW",
            "?operationName=Now&variables=%7B%22bannerPreset%22%3A%22266x266%22%2C%22stationId%22%3A7%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2295ed3dd1212114e94d459439bd60390b4d6f9e37b38baf8fd9653328ceb3b86b%22%7D%7D",  # noqa: E501
        )

    def get_current_track(self) -> Track:
        r = requests.get(
            url=f"{self.unnoficial_api}{self.unnoficial_api_operation_now}"
        )
        r.raise_for_status()
        song = r.json()["data"]["now"]["song"]

        song["artist"] = (
            song["interpreters"][0] if len(song["interpreters"]) > 0 else ""
        )

        song["cover_url"] = song["cover"]

        song["external_urls"] = {}
        for key, value in song["external_links"].items():
            if not (key.startswith("__") or value is None):
                song["external_urls"][key] = value["link"]

        # Special case uncountered once : album is none
        song["album"] = "" if song["album"] is None else song["album"]

        return Track(**song)


def convert_to_track(data: Dict[str, Any]) -> Track:
    track = data["track"]
    return Track(
        **{
            **track,
            "artist": track["mainArtists"][0]
            if "mainArtists" in track.keys() and len(track["mainArtists"]) > 0
            else "",
            "year": track["productionDate"],
            "album": track["albumTitle"],
        }
    )


def execute_grid_query(start: int, end: int, station: str = "FIP") -> List[Track]:
    logger.info(f"Querying the GraphQL API for {station} from {start} to {end}")
    query = f"""{{
            grid(start: {start}, end: {end}, station: {station}) {{
            ... on TrackStep {{
                track {{
                    title
                    albumTitle
                    mainArtists
                    productionDate
                    label
                    }}
                }}
            }}
        }}
    """
    res = requests.post(RADIO_FRANCE_API_URL, json={"query": query})
    res.raise_for_status()
    data = res.json()["data"]
    return [convert_to_track(t) for t in data["grid"]]


def execute_live_query(station: str = "FIP") -> Track:
    logger.info(f"Querying the GraphQL API for {station} from live")
    query = f"""{{
            live(station: {station}) {{
                song {{
                    id
                    track {{
                        title
                        albumTitle
                        mainArtists
                        productionDate
                        label
                    }}
                }}
            }}
        }}
        """
    res = requests.post(RADIO_FRANCE_API_URL, json={"query": query})
    res.raise_for_status()
    data = res.json()["data"]
    if data["live"]["song"] is None:
        raise LiveUnavailableException(
            (
                f"invalid result for live {station} query. "
                f"Status code '{res.status_code}' - {data}"
            )
        )
    return convert_to_track(data["live"]["song"])


def execute_stations_enum_query() -> List[Station]:
    logger.info("Querying the GraphQL API for all Radio France stations")
    query = '{__type(name: "StationsEnum") {enumValues {name}}}'
    res = requests.post(RADIO_FRANCE_API_URL, json={"query": query})
    res.raise_for_status()
    data = res.json()["data"]
    return [Station(name=station["name"]) for station in data["__type"]["enumValues"]]


def get_api_status() -> int:
    logger.info("Fetching api status")
    res = requests.post(
        url=RADIO_FRANCE_API_URL,
        json={
            "query": "{ __typename }",
        },
    )
    return res.status_code
