import os

import requests
from dotenv import load_dotenv
from loguru import logger

from whatsonfip.models import Track

load_dotenv()

SPOTIFY_API_HOST = os.getenv("SPOTIFY_API_HOST", "spotify-api")
SPOTIFY_API_PORT = os.getenv("SPOTIFY_API_PORT", "80")


class SpotifyTrackNotFound(Exception):
    """Raised when no track has been found for the query"""

    pass


def search_on_spotify(query: str) -> Track:
    logger.info(f"search for '{query}' on Spotify API")
    service_address = f"http://{SPOTIFY_API_HOST}:{SPOTIFY_API_PORT}/search"
    payload = {"q": query, "simple": True}  # Get a flat simple response
    r = requests.get(service_address, params=payload)
    if r.status_code == requests.codes.not_found:
        logger.info(f"no track found on Spotify with query '{query}'")
        raise SpotifyTrackNotFound("no track found on Spotify with query '{query}'")
    r.raise_for_status()
    return Track(**r.json())


def get_spotify_track(input_track: Track) -> Track:
    query = f"{input_track.title} {input_track.artist}"
    try:
        spotifyTrack = search_on_spotify(query)
    except SpotifyTrackNotFound:
        # Try with a shorted query
        query = (
            f"{' '.join(input_track.title.split()[:2])} "
            f"{' '.join(input_track.artist.split()[:2])}"
        )
        spotifyTrack = search_on_spotify(query)
    return spotifyTrack


def add_spotify_external_url(input_track: Track) -> Track:
    external_urls = input_track.external_urls
    try:
        spotifyTrack = get_spotify_track(input_track)
        if "spotify" in spotifyTrack.external_urls:
            logger.info("Adding a spotify url to track")
            external_urls["spotify"] = spotifyTrack.external_urls["spotify"]
    except SpotifyTrackNotFound:
        # already logged previously
        pass

    output_track = input_track.copy(deep=True)
    output_track.external_urls = external_urls
    return output_track
