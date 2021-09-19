import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger

from whatsonfip import radio_france_api
from whatsonfip.models import APIStatus, Message, Station, Track
from whatsonfip.radio_meuh_api import get_current_song as get_current_meuh
from whatsonfip.spotify_api import add_spotify_external_url
from whatsonfip.unofficial_api import get_now_unofficial

load_dotenv()

USE_UNOFFICIAL_API = os.getenv("USE_UNOFFICIAL_API", "true") in (
    "True",
    "true",
    "1",
)


app = FastAPI(
    title="What's on FIP ?",
    description="Let's find out what your listening on this eclectic radio!",
    version="0.1.0",
)


@app.get(
    "/live",
    response_model=Track,
    responses={
        219: {
            "model": Message,
            "description": "No information available about the current track",
        },
        200: {"description": "Current track live"},
    },
)
async def get_live(
    station: str = Query(
        "FIP",
        title="Station Name",
        description="Short name of the Radio France station",
    )
) -> Track:

    track = None

    # Use retro-engineered API if possible
    if station == "FIP" and USE_UNOFFICIAL_API:
        try:
            logger.info("Use unofficial API to fetch current track")
            track = get_now_unofficial()
        except Exception as e:
            logger.warning("Error while using unofficial API: " + str(e))

    if track is None:
        # Radio France OpenAPI api: less reliable and complete
        try:
            track = radio_france_api.execute_live_query(station)
        except radio_france_api.LiveUnavailableException as e:
            logger.warning(e)
            return JSONResponse(
                content=jsonable_encoder(
                    {
                        "message": (
                            "No information available about the "
                            f"current track at {station}"
                        )
                    }
                ),
                status_code=219,
            )

    # Add spotify external_url if necessary
    try:
        if not ("spotify" in track.external_urls):
            logger.info("Looking for the track on spotify")
            track = add_spotify_external_url(track)
    except Exception as e:
        logger.warning("Error while using spotify API: " + str(e))

    return track


@app.get("/grid", response_model=List[Track])
async def get_grid(start: int, end: int, station: str = "FIP") -> List[Track]:
    return radio_france_api.execute_grid_query(start, end, station)


@app.get("/stations", response_model=List[Station])
async def get_stations() -> List[Station]:
    return radio_france_api.execute_stations_enum_query()


@app.get("/health")
async def get_health():
    return {"message": "OK"}


@app.get("/api-status", response_model=APIStatus)
async def get_api_status():
    return {"code": radio_france_api.get_api_status()}


@app.get("/meuh", response_model=Track)
async def get_live_meuh() -> Track:
    track = get_current_meuh()
    # Add spotify external_url if necessary
    try:
        if not ("spotify" in track.external_urls):
            logger.info("Looking for the track on spotify")
            track = add_spotify_external_url(track)
    except Exception as e:
        logger.warning("Error while using spotify API: " + str(e))

    return track
