import spotipy
from dateparser import parse as date_parse
from loguru import logger
from spotipy import SpotifyClientCredentials

from whats_on_fip.models import Track

_sp: spotipy.Spotify | None = None


def _get_client() -> spotipy.Spotify:
    global _sp
    if _sp is None:
        _sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    return _sp


class SpotifyTrackNotFound(Exception):
    """Raised when no track has been found for the query"""

    pass


def search_on_spotify(query: str) -> Track:
    logger.info(f"search for '{query}' on Spotify API")
    sp = _get_client()
    res = sp.search(query, limit=1, offset=0, type="track")
    if not res or len(res["tracks"]["items"]) == 0:
        logger.info(f"no track found on Spotify with query '{query}'")
        raise SpotifyTrackNotFound(f"no track found on Spotify with query '{query}'")

    item = res["tracks"]["items"][0]
    artists = item.get("artists", [])
    album = item.get("album", {})
    release_date = album.get("release_date", "")
    year = date_parse(release_date).year if release_date else None

    return Track(
        title=item["name"],
        album=album.get("name"),
        artist=artists[0]["name"] if artists else "",
        year=year,
        external_urls=item.get("external_urls", {}),
    )


def get_spotify_track(input_track: Track) -> Track:
    query = f"{input_track.title} {input_track.artist}"
    try:
        return search_on_spotify(query)
    except SpotifyTrackNotFound:
        # Try with a shorter query
        query = f"{' '.join(input_track.title.split()[:2])} {' '.join(input_track.artist.split()[:2])}"
        return search_on_spotify(query)


def get_spotify_app_link(spotify_url: str) -> str:
    track_id = spotify_url.split("/")[-1]
    return f"spotify:track:{track_id}"


def get_spotify_url(spotify_track_id: str) -> str:
    return f"https://open.spotify.com/track/{spotify_track_id}"


def add_spotify_external_url(input_track: Track) -> Track:
    logger.info(f"Looking for track {input_track} on spotify")
    output_track = input_track.model_copy(deep=True)
    if "spotify" not in output_track.external_urls:
        try:
            spotify_track = get_spotify_track(input_track)
            if "spotify" in spotify_track.external_urls:
                logger.info("Adding a spotify url to track")
                output_track.external_urls["spotify"] = spotify_track.external_urls["spotify"]
        except SpotifyTrackNotFound:
            logger.warning(f"no spotify URL found for track {input_track}")

    if "spotify" in output_track.external_urls:
        output_track.external_urls["spotify_app"] = get_spotify_app_link(output_track.external_urls["spotify"])

    return output_track
