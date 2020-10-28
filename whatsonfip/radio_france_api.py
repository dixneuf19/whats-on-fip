import os
import logging
from typing import List

from dotenv import load_dotenv

from gql import gql, Client, AIOHTTPTransport
from requests.models import HTTPError
from requests import get

from whatsonfip.models import Song, Station

load_dotenv()

API_TOKEN = os.getenv("RADIO_FRANCE_API_TOKEN")

RADIO_FRANCE_API = os.getenv(
    "RADIO_FRANCE_API_HOST", "https://openapi.radiofrance.fr/v1/graphql"
)
RADIO_FRANCE_API_HEALTHCHECK = os.getenv(
    "RADIO_FRANCE_API_HEALTHCHECK",
    "https://openapi.radiofrance.fr/v1/.well-known/apollo/server-health",
)


class LiveUnavailableException(Exception):
    pass


def track_to_song(track) -> Song:
    doc = track["track"]
    artist = None
    try:
        artist = doc["mainArtists"][0]
    except IndexError:
        pass

    return Song(
        title=doc["title"],
        album=doc["albumTitle"],
        artist=artist,
        year=doc["productionDate"],
    )


class APIClient(Client):
    def __init__(self) -> None:
        try:
            logging.info("Initiating GraphQL API client")
            sample_transport = AIOHTTPTransport(
                url=f"{RADIO_FRANCE_API}?x-token={API_TOKEN}"
            )
            super().__init__(
                transport=sample_transport,
                fetch_schema_from_transport=True,
            )
        except HTTPError as e:
            if "403" in str(e):
                logging.warning("The API returned 403, check your API token")
            raise
        except:
            raise

    async def execute_grid_query(
        self, start: int, end: int, station: str = "FIP"
    ) -> List[Song]:
        logging.info(f"Querying the GraphQL API for {station} from {start} to {end}")
        query = gql(
            f"""{{ 
                grid(start: {start}, end: {end}, station: {station}) {{ 
                ... on TrackStep {{ 
                    track {{ 
                        title 
                        albumTitle 
                        mainArtists 
                        productionDate
                        }}
                    }} 
                }} 
            }} 
        """
        )
        try:
            tracks = await super().execute_async(query)
            return [track_to_song(t) for t in tracks["grid"]]
        except:
            raise

    async def execute_live_query(self, station: str = "FIP") -> Song:
        logging.info(f"Querying the GraphQL API for {station} from live")
        query = gql(
            f"""{{
                live(station: {station}) {{
                    song {{
                        id
                        track {{
                            title
                            albumTitle
                            mainArtists
                            productionDate
                        }}
                    }}
                }}
            }}
            """
        )
        res = await super().execute_async(query)
        if res["live"]["song"] is None:
            raise LiveUnavailableException(
                f"invalid result for live {station} query : {res}"
            )
        return track_to_song(res["live"]["song"])

    async def execute_stations_enum_query(self) -> List[Station]:
        logging.info(f"Querying the GraphQL API for all Radio France stations")
        query = gql('{__type(name: "StationsEnum") {enumValues {name}}}')
        try:
            res = await super().execute_async(query)
            return [
                Station(name=station["name"]) for station in res["__type"]["enumValues"]
            ]
        except:
            raise

    async def get_api_status(self) -> int:
        logging.info(f"Fetching api status")
        res = get(url=RADIO_FRANCE_API_HEALTHCHECK, params={"x-token": API_TOKEN})
        return res.status_code
