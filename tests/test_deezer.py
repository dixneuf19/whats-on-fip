import pytest

from whats_on_fip import deezer
from whats_on_fip.deezer import DeezerTrackNotFound, add_deezer_external_url, get_deezer_track, search_on_deezer
from whats_on_fip.models import Track

DEEZER_SEARCH_RESPONSES = {
    "logical song supertramp": {
        "data": [
            {
                "id": 2307846,
                "title": "The Logical Song",
                "link": "https://www.deezer.com/track/2307846",
                "artist": {"id": 1146, "name": "Supertramp"},
                "album": {"id": 219207, "title": "Breakfast In America"},
            }
        ]
    },
}


def _mock_deezer_get(responses):
    def _get(url, params=None):
        query = params.get("q", "") if params else ""
        data = responses.get(query, {"data": []})

        class FakeResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return data

        return FakeResponse()

    return _get


def test_search_on_deezer(mocker):
    mocker.patch.object(deezer._session, "get", new=_mock_deezer_get(DEEZER_SEARCH_RESPONSES))
    result = search_on_deezer("logical song supertramp")
    assert result["link"] == "https://www.deezer.com/track/2307846"


def test_search_on_deezer_not_found(mocker):
    mocker.patch.object(deezer._session, "get", new=_mock_deezer_get(DEEZER_SEARCH_RESPONSES))
    with pytest.raises(DeezerTrackNotFound):
        search_on_deezer("not this song for sure")


def test_get_deezer_track(mocker):
    mocker.patch.object(deezer._session, "get", new=_mock_deezer_get(DEEZER_SEARCH_RESPONSES))
    track = Track(title="logical song", artist="supertramp")
    url = get_deezer_track(track)
    assert url == "https://www.deezer.com/track/2307846"


def test_add_deezer_external_url(mocker):
    mocker.patch.object(deezer._session, "get", new=_mock_deezer_get(DEEZER_SEARCH_RESPONSES))
    track = Track(title="logical song", artist="supertramp")
    enriched = add_deezer_external_url(track)
    assert "deezer" in enriched.external_urls
    assert enriched.external_urls["deezer"] == "https://www.deezer.com/track/2307846"


def test_add_deezer_external_url_not_found(mocker):
    mocker.patch.object(deezer._session, "get", new=_mock_deezer_get(DEEZER_SEARCH_RESPONSES))
    track = Track(title="nonexistent", artist="nobody")
    enriched = add_deezer_external_url(track)
    assert "deezer" not in enriched.external_urls
    assert enriched == track


def test_add_deezer_external_url_already_existing(mocker):
    mocker.patch.object(deezer._session, "get", new=_mock_deezer_get(DEEZER_SEARCH_RESPONSES))
    track = Track(title="logical song", artist="supertramp", external_urls={"deezer": "https://existing.url"})
    enriched = add_deezer_external_url(track)
    assert enriched.external_urls["deezer"] == "https://existing.url"
