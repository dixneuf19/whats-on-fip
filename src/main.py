import logging
from typing import List

from fastapi import FastAPI, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.radio_france_api import APIClient, LiveUnavailableException
from src.models import Song, Station, APIStatus

app = FastAPI()
api_client = APIClient()


@app.get("/live", response_model=Song)
async def get_live(station: str = Query("FIP", title="Station Name", description="Short name of the Radio France station")) -> Song:
    try:
        return api_client.execute_live_query(station)
    except LiveUnavailableException as e:
        logging.warning(e)
        return JSONResponse(
            content=jsonable_encoder({"message": "No track information"}), status_code=status.HTTP_204_NO_CONTENT
        )


@app.get("/grid", response_model=List[Song])
async def get_grid(start: int, end: int, station: str = "FIP") -> List[Song]:
    return api_client.execute_grid_query(start, end, station)

@app.get("/stations", response_model=List[Station])
async def get_stations() -> List[Station]:
    return api_client.execute_stations_enum_query()

@app.get("/health")
async def get_health():
    return {"message": "OK"}

@app.get("/api-status", response_model=APIStatus)
async def get_api_status():
    return {"code": api_client.get_api_status()}
