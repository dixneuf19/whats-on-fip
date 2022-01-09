import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from loguru import logger

from whats_on_fip.models import Station, Track

load_dotenv()

API_TOKEN = os.getenv("RADIO_FRANCE_API_TOKEN")

RADIO_FRANCE_API_HOST = os.getenv(
    "RADIO_FRANCE_API_HOST", "https://openapi.radiofrance.fr/v1/graphql"
)
RADIO_FRANCE_API_HEALTHCHECK = os.getenv(
    "RADIO_FRANCE_API_HEALTHCHECK",
    "https://openapi.radiofrance.fr/v1/.well-known/apollo/server-health",
)

RADIO_FRANCE_API_URL = f"{RADIO_FRANCE_API_HOST}?x-token={API_TOKEN}"


class LiveUnavailableException(Exception):
    pass


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
    res = requests.get(url=RADIO_FRANCE_API_HEALTHCHECK, params={"x-token": API_TOKEN})
    return res.status_code
