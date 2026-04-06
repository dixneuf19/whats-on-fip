from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger

from whats_on_fip import radio_france_api
from whats_on_fip.models import APIStatus, Message, Station, Track
from whats_on_fip.radio_feelgood_api import RadioFeelGood
from whats_on_fip.radio_fiftyfifty import Radio5050
from whats_on_fip.radio_meuh_api import RadioMeuh
from whats_on_fip.spotify_api import add_spotify_external_url

app = FastAPI(
    title="What's on FIP ?",
    description="Let's find out what your listening on this eclectic radio!",
    version="0.1.0",
)


def _enrich_with_spotify(track: Track) -> Track:
    try:
        return add_spotify_external_url(track)
    except Exception as e:
        logger.warning("Error while using spotify API: " + str(e))
        return track


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
def get_live(
    station: str = Query(
        "FIP",
        title="Station Name",
        description="Short name of the Radio France station",
    ),
) -> Track | JSONResponse:
    try:
        track = radio_france_api.execute_live_query(station)
    except radio_france_api.LiveUnavailableException as e:
        logger.warning(e)
        return JSONResponse(
            content=jsonable_encoder({"message": f"No information available about the current track at {station}"}),
            status_code=219,
        )

    return _enrich_with_spotify(track)


@app.get("/grid", response_model=list[Track])
def get_grid(start: int, end: int, station: str = "FIP") -> list[Track]:
    return radio_france_api.execute_grid_query(start, end, station)


@app.get("/stations", response_model=list[Station])
def get_stations() -> list[Station]:
    return radio_france_api.execute_stations_enum_query()


@app.get("/health")
async def get_health() -> dict[str, str]:
    return {"message": "OK"}


@app.get("/api-status", response_model=APIStatus)
def get_api_status() -> dict[str, int]:
    return {"code": radio_france_api.get_api_status()}


@app.get("/meuh", response_model=Track)
def get_live_meuh() -> Track:
    return _enrich_with_spotify(RadioMeuh().get_current_track())


@app.get("/5050", response_model=Track)
def get_live_fiftyfifty() -> Track:
    return _enrich_with_spotify(Radio5050().get_current_track())


@app.get("/feelgood", response_model=Track)
def get_live_feelgood() -> Track:
    return _enrich_with_spotify(RadioFeelGood().get_current_track())
