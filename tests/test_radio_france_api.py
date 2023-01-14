from unittest.mock import ANY

import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils import generate_requests_get_mock, generate_requests_post_mock
from whats_on_fip.models import Track
from whats_on_fip.radio_france_api import (
    LiveUnavailableException,
    RadioFIP,
    execute_grid_query,
    execute_live_query,
    execute_stations_enum_query,
    get_api_status,
)

radio_france_stations = [
    "ELSASS",
    "FIP",
    "FIP_BORDEAUX",
    "FIP_ELECTRO",
    "FIP_GROOVE",
    "FIP_JAZZ",
    "FIP_METAL",
    "FIP_NANTES",
    "FIP_NOUVEAUTES",
    "FIP_POP",
    "FIP_REGGAE",
    "FIP_ROCK",
    "FIP_STRASBOURG",
    "FIP_WORLD",
    "FORMATION",
    "FRANCEBLEU",
    "FRANCEBLEU_ALSACE",
    "FRANCEBLEU_ARMORIQUE",
    "FRANCEBLEU_AUXERRE",
    "FRANCEBLEU_AZUR",
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
    "FRANCEBLEU_LORRAINE_NORD",
    "FRANCEBLEU_MAINE",
    "FRANCEBLEU_MAYENNE",
    "FRANCEBLEU_NORD",
    "FRANCEBLEU_NORMANDIE_CAEN",
    "FRANCEBLEU_NORMANDIE_ROUEN",
    "FRANCEBLEU_ORLEANS",
    "FRANCEBLEU_PARIS",
    "FRANCEBLEU_PAYS_BASQUE",
    "FRANCEBLEU_PAYS_DE_SAVOIE",
    "FRANCEBLEU_PAYS_D_AUVERGNE",
    "FRANCEBLEU_PERIGORD",
    "FRANCEBLEU_PICARDIE",
    "FRANCEBLEU_POITOU",
    "FRANCEBLEU_PROVENCE",
    "FRANCEBLEU_RCFM",
    "FRANCEBLEU_ROUSSILLON",
    "FRANCEBLEU_SAINT_ETIENNE_LOIRE",
    "FRANCEBLEU_SUR_LORRAINE",
    "FRANCEBLEU_TOULOUSE",
    "FRANCEBLEU_TOURAINE",
    "FRANCEBLEU_VAUCLUSE",
    "FRANCECULTURE",
    "FRANCEINFO",
    "FRANCEINTER",
    "FRANCEMUSIC",
    "FRANCEMUSIQUE",
    "FRANCEMUSIQUE_CLASSIQUE_EASY",
    "FRANCEMUSIQUE_CLASSIQUE_PLUS",
    "FRANCEMUSIQUE_CONCERT_RF",
    "FRANCEMUSIQUE_EVENEMENTIELLE",
    "FRANCEMUSIQUE_LA_CONTEMPORAINE",
    "FRANCEMUSIQUE_LA_JAZZ",
    "FRANCEMUSIQUE_OCORA_MONDE",
    "MOUV",
    "MOUV_100MIX",
    "MOUV_CLASSICS",
    "MOUV_DANCEHALL",
    "MOUV_RAPFR",
    "MOUV_RAPUS",
    "MOUV_RNB",
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
    assert [station.name for station in response] == radio_france_stations


def test_get_api_status():
    response = get_api_status()
    assert response in (200, 500)


unnoficial_api_example_response = {
    "data": {
        "now": {
            "__typename": "Now",
            "playing_item": {
                "__typename": "TimelineItem",
                "title": "Shawn Lee",
                "subtitle": "Laurel canyon",
                "cover": "https://cdn.radiofrance.fr/s3/cruiser-production/2019/11/e976fa6a-5274-4590-a592-3936a5e193ef/266x266_rf_omm_0000178469_dnc.0057698852.jpg",  # noqa:E501
                "start_time": 1644953615,
                "end_time": 1644953751,
                "year": 2005,
            },
            "program": None,
            "song": {
                "__typename": "SongOnAir",
                "uuid": "0d4b0912-d0b4-4a29-a6ae-e29d941ddd90",
                "cover": "https://cdn.radiofrance.fr/s3/cruiser-production/2019/11/e976fa6a-5274-4590-a592-3936a5e193ef/266x266_rf_omm_0000178469_dnc.0057698852.jpg",  # noqa:E501
                "title": "Laurel canyon",
                "interpreters": ["Shawn Lee"],
                "musical_kind": "Jazz ",
                "label": "UBIQUITY",
                "album": "Moods and grooves",
                "year": 2005,
                "external_links": {
                    "youtube": None,
                    "deezer": {
                        "id": "983830942",
                        "link": "https://www.deezer.com/track/983830942",
                        "image": "https://e-cdns-images.dzcdn.net/images/cover/c0b6f8daad635988cd595a16fefc655b/1000x1000-000000-80-0-0.jpg",  # noqa:E501
                        "__typename": "ExternalLink",
                    },
                    "itunes": {
                        "id": "1517131275",
                        "link": "https://music.apple.com/fr/album/laurel-canyon/1517130920?i=1517131275&uo=4",  # noqa:E501
                        "image": "https://is2-ssl.mzstatic.com/image/thumb/Music113/v4/a4/97/43/a49743f3-9958-205a-b025-a1fd1003c7ea/source/100x100bb.jpg",  # noqa:E501
                        "__typename": "ExternalLink",
                    },
                    "spotify": {
                        "id": "6cxTGlQRrT5ZNlsNF3dMen",
                        "link": "https://open.spotify.com/track/6cxTGlQRrT5ZNlsNF3dMen",
                        "image": "https://i.scdn.co/image/ab67616d0000b273298dde4e833624a6591f42c2",  # noqa:E501
                        "__typename": "ExternalLink",
                    },
                    "__typename": "ExternalLinks",
                },
            },
            "server_time": 1644953628,
            "next_refresh": 1644953752,
            "mode": "song",
        }
    }
}

unnoficial_api_example_expected = Track(
    title="Laurel canyon",
    album="Moods and grooves",
    artist="Shawn Lee",
    year=2005,
    label="UBIQUITY",
    musical_kind="Jazz ",
    external_urls={
        "deezer": "https://www.deezer.com/track/983830942",
        "itunes": "https://music.apple.com/fr/album/laurel-canyon/1517130920?i=1517131275&uo=4",  # noqa:E501
        "spotify": "https://open.spotify.com/track/6cxTGlQRrT5ZNlsNF3dMen",
    },
    cover_url="https://cdn.radiofrance.fr/s3/cruiser-production/2019/11/e976fa6a-5274-4590-a592-3936a5e193ef/266x266_rf_omm_0000178469_dnc.0057698852.jpg",  # noqa:E501
)


@pytest.mark.asyncio
async def test_get_now_unofficial():
    assert Track(**RadioFIP().get_current_track().dict())


@pytest.mark.asyncio
async def test_get_now_unofficial_with_cover():
    """
    Test the assumption that when the unofficial API works, there is always a cover
    """
    assert Track(**RadioFIP().get_current_track().dict()).cover_url is not None


def test_get_now_unofficial_mocked(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock(unnoficial_api_example_response),
    )
    assert RadioFIP().get_current_track() == unnoficial_api_example_expected
