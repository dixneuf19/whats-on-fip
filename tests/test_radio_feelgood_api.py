import pytest

from tests.utils import generate_requests_get_mock
from whats_on_fip.models import Track
from whats_on_fip.radio_feelgood_api import RadioFeelGood

EXAMPLE_FEELGOOD_API_RESPONSE = [
    {
        "__typename": "TitleDiffusion",
        "id": "bY9g69qnJA",
        "timestamp": "2022-05-10T17:27:36.149Z",
        "mdsId": "2174546520932614607",
        "title": {
            "__typename": "Title",
            "id": "j5gq4Gxs7G",
            "title": "SAM FELDT",
            "artist": "HAPPY HOUR DJ",
            "coverUrl": "https://www.lesindesradios.fr/servicesimb/images?version=6&iid=h/ha/happyhourdj/samfeldt&width=300",  # noqa:E501
            "spotifyId": None,
            "deezerId": None,
            "coverId": "h/ha/happyhourdj/samfeldt",
        },
    }
]

EXPECTED_TRACK_OBJECT = Track(
    title="SAM FELDT",
    artist="HAPPY HOUR DJ",
    cover_url="https://images.lesindesradios.fr/fit-in/300x2000/filters:quality(100)/radios/radiofg/radiostream/5gWkrl9VKE/vignette_awN7JwWOid.jpeg",  # noqa:E501
)


@pytest.mark.asyncio
async def test_get_current_song_remote():
    assert Track(**RadioFeelGood().get_current_track().dict())


def test_get_current_song_mocked(mocker):
    mocker.patch(
        "requests.get", new=generate_requests_get_mock(EXAMPLE_FEELGOOD_API_RESPONSE)
    )
    track = RadioFeelGood().get_current_track()
    assert track == EXPECTED_TRACK_OBJECT
