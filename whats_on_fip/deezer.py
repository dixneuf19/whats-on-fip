import niquests
from loguru import logger

from whats_on_fip.models import Track

DEEZER_API_URL = "https://api.deezer.com/search"

_session = niquests.Session()


class DeezerTrackNotFound(Exception):
    pass


def search_on_deezer(query: str) -> dict:
    logger.info(f"search for '{query}' on Deezer")
    res = _session.get(DEEZER_API_URL, params={"q": query})
    res.raise_for_status()
    data = res.json().get("data", [])
    if not data:
        raise DeezerTrackNotFound(f"no track found on Deezer with query '{query}'")
    return data[0]


def get_deezer_track(input_track: Track) -> str:
    query = f"{input_track.title} {input_track.artist}"
    try:
        result = search_on_deezer(query)
    except DeezerTrackNotFound:
        query = f"{' '.join(input_track.title.split()[:2])} {' '.join(input_track.artist.split()[:2])}"
        result = search_on_deezer(query)
    return result["link"]


def add_deezer_external_url(input_track: Track) -> Track:
    logger.info(f"Looking for track {input_track} on Deezer")
    if "deezer" in input_track.external_urls:
        return input_track
    output_track = input_track.model_copy(deep=True)
    try:
        deezer_url = get_deezer_track(input_track)
        output_track.external_urls["deezer"] = deezer_url
    except DeezerTrackNotFound:
        logger.warning(f"no Deezer URL found for track {input_track}")
    return output_track
