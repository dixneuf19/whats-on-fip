import pytest

from tests.utils import generate_requests_get_mock
from whats_on_fip.models import Track
from whats_on_fip.unofficial_api import get_now_unofficial

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
    assert Track(**get_now_unofficial().dict())


@pytest.mark.asyncio
async def test_get_now_unofficial_with_cover():
    """
    Test the assumption that when the unofficial API works, there is always a cover
    """
    assert Track(**get_now_unofficial().dict()).cover_url is not None


def test_get_now_unofficial_mocked(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock(unnoficial_api_example_response),
    )
    assert get_now_unofficial() == unnoficial_api_example_expected
