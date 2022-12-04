import pytest

from tests.utils import generate_requests_get_mock
from whats_on_fip.models import Track
from whats_on_fip.radio_meuh_api import RadioMeuh

EXAMPLE_MEUH_API_RESPONSE = [
    {
        "pos": 1,
        "imgSrc": None,
        "time": "15:14:53",
        "artist": "Steve Lacy",
        "album": "Apollo XXI",
        "titre": "Amandla's Interlude",
        "url": "https://www.dixneuf19.me",
        "expire": 159,
        "id": "27467",
    },
    {
        "pos": 2,
        "imgSrc": None,
        "time": "15:17:51",
        "artist": "Wolfgang Maus Soundpicture",
        "album": "",
        "titre": "Friendly Vibrations",
        "url": "https://www.dixneuf19.me",
        "expire": "",
        "id": "27044",
    },
]

EXPECTED_TRACK_OBJECT = Track(
    title="Amandla's Interlude",
    album="Apollo XXI",
    artist="Steve Lacy",
    external_urls={"spotify": "https://www.dixneuf19.me"},
)


@pytest.mark.asyncio
async def test_get_current_song_remote():
    assert Track(**RadioMeuh().get_current_track().dict())


def test_get_current_song_mocked(mocker):
    mocker.patch(
        "requests.get", new=generate_requests_get_mock(EXAMPLE_MEUH_API_RESPONSE)
    )
    track = RadioMeuh().get_current_track()
    assert track == EXPECTED_TRACK_OBJECT
