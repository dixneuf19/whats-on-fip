from unittest.mock import ANY

import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils import generate_requests_post_mock
from whats_on_fip.models import Station, Track
from whats_on_fip.radio_france_api import (
    LiveUnavailableException,
    execute_grid_query,
    execute_live_query,
    execute_stations_enum_query,
    get_api_status,
)

FIP_songs_2020_05_20_11h_12h_UTC = [
    {
        "title": "Distant land",
        "album": "Shades of blue",
        "artist": "Madlib",
        "year": 2003,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Distant land",
        "album": "Shades of blue",
        "artist": "Madlib",
        "year": 2003,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "The world is yours",
        "album": "Illmatic",
        "artist": "Nas",
        "year": 1994,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Build a nest (feat. Ruby Parker)",
        "album": "Suite for Max Brown",
        "artist": "Jeff Parker & The New Breed",
        "year": 2020,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Jeux d'eaux",
        "album": "Maurice Ravel : Oeuvre complete pour piano",
        "artist": "Jean-Efflam Bavouzet",
        "year": 2003,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Les deux hérons",
        "album": "Les atomes",
        "artist": "Martin Leon",
        "year": 2010,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Too young to be one",
        "album": "Happy together",
        "artist": "The Turtles",
        "year": 1967,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Swlabr",
        "album": "Disraeli gears",
        "artist": "Cream",
        "year": 1967,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Humpin",
        "album": "Best of",
        "artist": "The Bar Kays",
        "year": 1969,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Say it loud - I'm black and i'm proud",
        "album": "Say it loud - i'm black and i'm proud",
        "artist": "James Brown",
        "year": 1968,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Bruce Lee",
        "album": "Bruce Lee",
        "artist": "Catastrophe",
        "year": 2019,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Stoney street",
        "album": "Bricolage",
        "artist": "Amon Tobin",
        "year": 1997,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Hungboo",
        "album": "Nova autour du monde cd 5 : Asie",
        "artist": "Peggy Gou",
        "year": 2019,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Butterfly san",
        "album": "Tokyo city pop 70's",
        "artist": "Haruomi Hosono",
        "year": 1976,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Girl from Mill Valley",
        "album": "Beck-ola",
        "artist": "Jeff Beck",
        "year": 1969,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Wild horses",
        "album": "Sticky fingers (remasters)",
        "artist": "The Rolling Stones",
        "year": 1971,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
    {
        "title": "Cassidy",
        "album": "The true story of Molly Jin & June Cooper",
        "artist": "The Buns",
        "year": 2014,
        "musical_kind": None,
        "external_urls": {},
        "label": ANY,
        "cover_url": None,
    },
]


@pytest.mark.skip(reason="RadioFrance OpenAPI is unreliable")
def test_execute_grid_query():
    response = execute_grid_query(1589972400, 1589976000, "FIP")
    assert jsonable_encoder(response) == FIP_songs_2020_05_20_11h_12h_UTC


def test_execute_live_query():
    try:
        response = execute_live_query("FIP")
    except LiveUnavailableException:
        return
    assert Track(**response.dict())


def test_execute_live_query_with_exception(mocker):
    mocker.patch(
        "requests.post",
        new=generate_requests_post_mock({"data": {"live": {"song": None}}}, 200),
    )
    with pytest.raises(LiveUnavailableException):
        execute_live_query("FIP")


def test_execute_stations_enum_query():
    response = execute_stations_enum_query()
    assert Station(name="FIP") in response


def test_get_api_status():
    response = get_api_status()
    assert response in (200, 500)
