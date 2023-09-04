import pytest
from fastapi.testclient import TestClient

from tests.test_spotify_api import simple_queries_responses
from whats_on_fip.main import app
from whats_on_fip.models import Station, Track
from whats_on_fip.radio_france_api import LiveUnavailableException

client = TestClient(app)


def test_get_live(mocker):
    mocker.patch(
        "whats_on_fip.spotify_api.get_spotify_track",
        return_value=simple_queries_responses["logical song supertramp"],
    )
    response = client.get("/live")
    assert response.status_code in (200, 219)
    if response.status_code == 200:
        assert Track(**response.json())


def test_get_live_mocked(mocker):
    mocker.patch(
        "whats_on_fip.spotify_api.get_spotify_track",
        return_value=simple_queries_responses["logical song supertramp"],
    )
    response = client.get("/live")
    assert response.status_code == 200
    assert Track(**response.json())

    mocker.patch(
        "whats_on_fip.main.radio_france_api.execute_live_query",
        side_effect=LiveUnavailableException(),
    )
    response = client.get("/live")
    assert response.status_code == 219


@pytest.mark.skip(reason="RadioFrance OpenAPI is unreliable")
def test_get_grid():
    response = client.get(
        "/grid", params={"start": 1589972400, "end": 1589976000, "station": "FIP"}
    )
    assert response.status_code == 200
    if response.status_code == 200:
        assert [Track(**t) for t in response.json()]


def test_get_stations():
    response = client.get("/stations")
    assert response.status_code == 200
    assert [Station(**s) for s in response.json()]


def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_api_status():
    response = client.get("/api-status")
    assert response.status_code == 200
    assert response.json()["code"] in (200, 500)


def test_get_live_meuh(mocker):
    mocker.patch(
        "whats_on_fip.spotify_api.get_spotify_track",
        return_value=simple_queries_responses["logical song supertramp"],
    )
    response = client.get("/meuh")
    assert response.status_code == 200
    assert Track(**response.json())


def test_get_live_fiftyfifty(mocker):
    mocker.patch(
        "whats_on_fip.spotify_api.get_spotify_track",
        return_value=simple_queries_responses["logical song supertramp"],
    )
    response = client.get("/5050")
    assert response.status_code == 200
    assert Track(**response.json())


def test_get_live_feelgood(mocker):
    mocker.patch(
        "whats_on_fip.spotify_api.get_spotify_track",
        return_value=simple_queries_responses["logical song supertramp"],
    )
    response = client.get("/feelgood")
    assert response.status_code == 200
    assert Track(**response.json())
