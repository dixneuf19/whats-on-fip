from typing import Any, Callable, Dict

import pytest
from requests import Response, get

from tests.utils import generate_requests_get_mock
from whats_on_fip.models import Track
from whats_on_fip.spotify_api import (
    SpotifyTrackNotFound,
    add_spotify_external_url,
    get_spotify_app_link,
    get_spotify_track,
    get_spotify_url,
    search_on_spotify,
)

simple_queries_responses = {
    "logical song supertramp": {
        "album": "Breakfast In America (Deluxe Edition)",
        "year": 1979,
        "artist": "Supertramp",
        "title": "The Logical Song - Remastered 2010",
        "external_urls": {
            "spotify": "https://open.spotify.com/track/6mHOcVtsHLMuesJkswc0GZ",
            "spotify_app": "spotify:track:6mHOcVtsHLMuesJkswc0GZ",
        },
    },
    'album:"logical song" year:1979': {
        "album": "The Logical Song",
        "year": 1979,
        "artist": "Supertramp",
        "title": "The Logical Song",
        "external_urls": {
            "spotify": "https://open.spotify.com/track/4se2fj5uRWlkcnfhtnRLrZ",
            "spotify_app": "spotify:track:4se2fj5uRWlkcnfhtnRLrZ",
        },
    },
}


def generate_requests_get_mock_spotify_api(
    resp_by_queries: Dict[str, Dict[str, Any]]
) -> Callable[[str, Dict[str, Any]], Response]:
    def request_get_spotify_api(url: str, params: Dict[str, Any]) -> Response:
        query = params["q"]
        if query in simple_queries_responses:
            request_get_func = generate_requests_get_mock(
                simple_queries_responses[query], 200
            )
        else:
            request_get_func = generate_requests_get_mock({}, 404)
        return request_get_func(url, params)

    return request_get_spotify_api


def test_search_on_spotify(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )
    for query in simple_queries_responses.keys():
        assert search_on_spotify(query) == Track(**simple_queries_responses[query])


def test_search_on_spotify_unknow_track(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )
    with pytest.raises(SpotifyTrackNotFound):
        search_on_spotify("not this song on spotify for sure")


def test_get_spotify_track(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )

    output_track = Track(**simple_queries_responses["logical song supertramp"])

    # Exact match title + supertramp
    input_track = Track(
        title="logical song",
        album="Breakfeast in America",
        artist="supertramp",
    )
    assert get_spotify_track(input_track) == output_track

    # Match when limiting to 2 words
    input_track = Track(
        title="logical song remastered",
        album="Breakfeast in America",
        artist="supertramp",
    )
    assert get_spotify_track(input_track) == output_track


def test_get_spotify_track_unknown(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )
    input_track = Track(
        title="This",
        album="song",
        artist="does",
        musical_kind="not",
        label="exist",
    )
    with pytest.raises(SpotifyTrackNotFound):
        get_spotify_track(input_track)


def test_get_spotify_app_link():
    for t in simple_queries_responses.values():
        if "spotify" in t["external_urls"]:
            assert t["external_urls"]["spotify_app"] == get_spotify_app_link(
                t["external_urls"]["spotify"]
            )


def test_add_spotify_external_url(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )
    input_track_dict = {
        "title": "logical song",
        "album": "Breakfeast in America",
        "artist": "supertramp",
    }
    input_track = Track(**input_track_dict)

    output_track = Track(
        **input_track_dict,
        external_urls=simple_queries_responses["logical song supertramp"][
            "external_urls"
        ]
    )

    assert add_spotify_external_url(input_track) == output_track


def test_add_spotify_external_url_unknow(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )
    input_track = Track(
        title="This",
        album="song",
        artist="does",
        musical_kind="not",
        label="exist",
    )

    assert add_spotify_external_url(input_track) == input_track


def test_add_spotify_external_url_already_existing(mocker):
    mocker.patch(
        "requests.get",
        new=generate_requests_get_mock_spotify_api(simple_queries_responses),
    )
    input_track = Track(
        title="logical song",
        album="Breakfeast in America",
        artist="supertramp",
        external_urls={"spotify": "https://open.spotify.com/track/random-valid-id"},
    )

    output_track = input_track.copy(deep=True)
    output_track.external_urls["spotify_app"] = get_spotify_app_link(
        input_track.external_urls["spotify"]
    )

    assert add_spotify_external_url(input_track) == output_track


def test_get_spotify_url():
    arbitrary_spotify_id = "6mHOcVtsHLMuesJkswc0GZ"
    res = get(get_spotify_url(arbitrary_spotify_id))
    res.raise_for_status()
