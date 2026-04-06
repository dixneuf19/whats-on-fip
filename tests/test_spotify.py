import pytest
from requests import get

from whats_on_fip.models import Track
from whats_on_fip.spotify import (
    SpotifyTrackNotFound,
    add_spotify_external_url,
    get_spotify_app_link,
    get_spotify_track,
    get_spotify_url,
    search_on_spotify,
)

# Raw Spotify API response format (what spotipy.Spotify.search returns)
spotify_search_responses = {
    "logical song supertramp": {
        "tracks": {
            "items": [
                {
                    "name": "The Logical Song - Remastered 2010",
                    "album": {
                        "name": "Breakfast In America (Deluxe Edition)",
                        "release_date": "1979-03-29",
                        "external_urls": {"spotify": "https://open.spotify.com/album/xxx"},
                        "href": "https://api.spotify.com/v1/albums/xxx",
                        "id": "xxx",
                        "images": [],
                        "uri": "spotify:album:xxx",
                    },
                    "artists": [
                        {
                            "name": "Supertramp",
                            "external_urls": {"spotify": "https://open.spotify.com/artist/xxx"},
                            "href": "https://api.spotify.com/v1/artists/xxx",
                            "id": "xxx",
                            "uri": "spotify:artist:xxx",
                        }
                    ],
                    "external_urls": {"spotify": "https://open.spotify.com/track/6mHOcVtsHLMuesJkswc0GZ"},
                    "duration_ms": 252000,
                    "href": "https://api.spotify.com/v1/tracks/6mHOcVtsHLMuesJkswc0GZ",
                    "id": "6mHOcVtsHLMuesJkswc0GZ",
                    "preview_url": None,
                    "uri": "spotify:track:6mHOcVtsHLMuesJkswc0GZ",
                }
            ]
        }
    },
}

expected_tracks = {
    "logical song supertramp": Track(
        title="The Logical Song - Remastered 2010",
        album="Breakfast In America (Deluxe Edition)",
        artist="Supertramp",
        year=1979,
        external_urls={"spotify": "https://open.spotify.com/track/6mHOcVtsHLMuesJkswc0GZ"},
    ),
}


def _mock_spotify_search(query_responses):
    def _search(query, limit=1, offset=0, type="track"):
        if query in query_responses:
            return query_responses[query]
        return {"tracks": {"items": []}}

    return _search


def test_search_on_spotify(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    track = search_on_spotify("logical song supertramp")
    assert track == expected_tracks["logical song supertramp"]


def test_search_on_spotify_unknown_track(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    with pytest.raises(SpotifyTrackNotFound):
        search_on_spotify("not this song on spotify for sure")


def test_get_spotify_track(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    output_track = expected_tracks["logical song supertramp"]

    # Exact match
    input_track = Track(title="logical song", album="Breakfast in America", artist="supertramp")
    assert get_spotify_track(input_track) == output_track

    # Match when limiting to 2 words
    input_track = Track(title="logical song remastered", album="Breakfast in America", artist="supertramp")
    assert get_spotify_track(input_track) == output_track


def test_get_spotify_track_unknown(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    input_track = Track(title="This", album="song", artist="does", musical_kind="not", label="exist")
    with pytest.raises(SpotifyTrackNotFound):
        get_spotify_track(input_track)


def test_get_spotify_app_link():
    assert (
        get_spotify_app_link("https://open.spotify.com/track/6mHOcVtsHLMuesJkswc0GZ")
        == "spotify:track:6mHOcVtsHLMuesJkswc0GZ"
    )


def test_add_spotify_external_url(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    input_track = Track(title="logical song", album="Breakfast in America", artist="supertramp")
    output_track = add_spotify_external_url(input_track)

    assert "spotify" in output_track.external_urls
    assert "spotify_app" in output_track.external_urls
    assert output_track.external_urls["spotify"] == "https://open.spotify.com/track/6mHOcVtsHLMuesJkswc0GZ"
    assert output_track.external_urls["spotify_app"] == "spotify:track:6mHOcVtsHLMuesJkswc0GZ"


def test_add_spotify_external_url_unknown(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    input_track = Track(title="This", album="song", artist="does", musical_kind="not", label="exist")
    assert add_spotify_external_url(input_track) == input_track


def test_add_spotify_external_url_already_existing(mocker):
    mocker.patch(
        "whats_on_fip.spotify._get_client",
        return_value=mocker.Mock(search=_mock_spotify_search(spotify_search_responses)),
    )
    input_track = Track(
        title="logical song",
        album="Breakfast in America",
        artist="supertramp",
        external_urls={"spotify": "https://open.spotify.com/track/random-valid-id"},
    )
    output_track = add_spotify_external_url(input_track)
    assert output_track.external_urls["spotify"] == "https://open.spotify.com/track/random-valid-id"
    assert output_track.external_urls["spotify_app"] == "spotify:track:random-valid-id"


def test_get_spotify_url():
    arbitrary_spotify_id = "6mHOcVtsHLMuesJkswc0GZ"
    res = get(get_spotify_url(arbitrary_spotify_id))
    res.raise_for_status()
