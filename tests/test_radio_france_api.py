from unittest.mock import ANY

import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils import generate_requests_post_mock
from whatsonfip.models import Track
from whatsonfip.radio_france_api import (
    LiveUnavailableException,
    execute_grid_query,
    execute_live_query,
    execute_stations_enum_query,
    get_api_status,
)

radio_france_stations = [
    "FRANCEINTER",
    "FRANCEINFO",
    "FRANCEBLEU",
    "FRANCEMUSIQUE",
    "FRANCECULTURE",
    "MOUV",
    "FIP",
    "FRANCEBLEU_RCFM",
    "FRANCEBLEU_ALSACE",
    "FRANCEBLEU_ARMORIQUE",
    "FRANCEBLEU_AUXERRE",
    "FRANCEBLEU_BEARN",
    "FRANCEBLEU_BELFORT_MONTBELIARD",
    "FRANCEBLEU_BERRY",
    "FRANCEBLEU_BESANCON",
    "FRANCEBLEU_BOURGOGNE",
    "FRANCEBLEU_BREIZH_IZEL",
    "FRANCEBLEU_CHAMPAGNE_ARDENNE",
    "FRANCEBLEU_COTENTIN",
    "FRANCEBLEU_CREUSE",
    "FRANCEBLEU_DROME_ARDECHE",
    "FRANCEBLEU_GARD_LOZERE",
    "FRANCEBLEU_GASCOGNE",
    "FRANCEBLEU_GIRONDE",
    "FRANCEBLEU_HERAULT",
    "FRANCEBLEU_ISERE",
    "FRANCEBLEU_LA_ROCHELLE",
    "FRANCEBLEU_LIMOUSIN",
    "FRANCEBLEU_LOIRE_OCEAN",
    "FRANCEBLEU_SUR_LORRAINE",
    "FRANCEBLEU_MAYENNE",
    "FRANCEBLEU_NORD",
    "FRANCEBLEU_NORMANDIE_CAEN",
    "FRANCEBLEU_NORMANDIE_ROUEN",
    "FRANCEBLEU_ORLEANS",
    "FRANCEBLEU_PAYS_D_AUVERGNE",
    "FRANCEBLEU_PAYS_BASQUE",
    "FRANCEBLEU_PAYS_DE_SAVOIE",
    "FRANCEBLEU_PERIGORD",
    "FRANCEBLEU_PICARDIE",
    "FRANCEBLEU_PROVENCE",
    "FRANCEBLEU_ROUSSILLON",
    "FRANCEBLEU_TOURAINE",
    "FRANCEBLEU_VAUCLUSE",
    "FRANCEBLEU_AZUR",
    "FRANCEBLEU_LORRAINE_NORD",
    "FRANCEBLEU_POITOU",
    "FIP_BORDEAUX",
    "FIP_NANTES",
    "FIP_STRASBOURG",
    "FIP_ROCK",
    "FIP_JAZZ",
    "FIP_GROOVE",
    "FRANCEBLEU_PARIS",
    "FIP_WORLD",
    "FIP_NOUVEAUTES",
    "FIP_REGGAE",
    "FIP_ELECTRO",
    "MOUV_100MIX",
    "FIP_METAL",
    "FIP_POP",
    "MOUV_CLASSICS",
    "MOUV_DANCEHALL",
    "MOUV_RNB",
    "MOUV_RAPUS",
    "MOUV_RAPFR",
    "ELSASS",
    "FRANCEBLEU_MAINE",
    "FRANCEBLEU_TOULOUSE",
    "FRANCEBLEU_SAINT_ETIENNE_LOIRE",
    "FORMATION",
    "FRANCEMUSIQUE_CLASSIQUE_EASY",
    "FRANCEMUSIQUE_CLASSIQUE_PLUS",
    "FRANCEMUSIQUE_CONCERT_RF",
    "FRANCEMUSIQUE_OCORA_MONDE",
    "FRANCEMUSIQUE_LA_JAZZ",
    "FRANCEMUSIQUE_LA_CONTEMPORAINE",
    "FRANCEMUSIQUE_EVENEMENTIELLE",
    "FRANCEMUSIC",
]

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
    assert [station.name for station in response] == radio_france_stations


def test_get_api_status():
    response = get_api_status()
    assert response in (200, 500)
