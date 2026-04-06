from telegram.helpers import escape_markdown

from whats_on_fip.models import FIP_RADIO, Radio, Track

LINK_PROVIDERS = ["deezer", "spotify", "youtube", "itunes"]


def track_to_markdown(track: Track, radio: Radio = FIP_RADIO) -> str:
    # Radio name needs manual escaping since it's in a markdown link
    radio_name = radio.name.replace("-", r"\-")
    md = f"*Live on [{radio_name}]({radio.url}) :*\n\n"

    md += "*" + escape_markdown(track.title, version=2) + "*\n"
    md += "_" + escape_markdown(track.artist, version=2) + "_\n"
    if track.album is not None:
        md += escape_markdown(track.album, version=2)
    if track.album is not None and track.year is not None:
        md += r" \- "
    if track.year is not None:
        md += escape_markdown(str(track.year), version=2)

    # Add first available provider link
    for provider in LINK_PROVIDERS:
        if provider in track.external_urls:
            url = track.external_urls[provider]
            md += f"\n\n[{escape_markdown(provider.title(), version=2)}]({url})"
            break

    return md
