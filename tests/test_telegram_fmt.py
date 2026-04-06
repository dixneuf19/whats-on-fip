from whats_on_fip.models import FEELGOOD_RADIO, MEUH_RADIO, Track
from whats_on_fip.telegram.fmt import track_to_markdown


def test_track_to_markdown_full():
    track = Track(
        title="The Logical Song",
        artist="Supertramp",
        album="Breakfast In America",
        year=1979,
        external_urls={"deezer": "https://www.deezer.com/track/123"},
    )
    md = track_to_markdown(track)
    assert "*Live on [FIP](https://www.fip.fr) :*" in md
    assert "*The Logical Song*" in md
    assert "_Supertramp_" in md
    assert "Breakfast In America" in md
    assert "1979" in md
    assert "[Deezer](https://www.deezer.com/track/123)" in md


def test_track_to_markdown_no_album_no_year():
    track = Track(title="Mystery Song", artist="Unknown Artist")
    md = track_to_markdown(track)
    assert "*Mystery Song*" in md
    assert "_Unknown Artist_" in md
    assert r"\-" not in md


def test_track_to_markdown_with_radio():
    track = Track(title="Test", artist="Artist")
    md = track_to_markdown(track, radio=MEUH_RADIO)
    assert "Radiomeuh" in md
    assert "radiomeuh.com" in md


def test_track_to_markdown_feelgood_radio():
    track = Track(title="Test", artist="Artist")
    md = track_to_markdown(track, radio=FEELGOOD_RADIO)
    assert "Radio FG" in md
    assert "Feel Good" in md


def test_track_to_markdown_no_link():
    track = Track(title="Song", artist="Artist", year=2020)
    md = track_to_markdown(track)
    assert "Deezer" not in md
    assert "Spotify" not in md


def test_track_to_markdown_deezer_preferred_over_spotify():
    track = Track(
        title="Song",
        artist="Artist",
        external_urls={
            "spotify": "https://open.spotify.com/track/123",
            "deezer": "https://www.deezer.com/track/456",
        },
    )
    md = track_to_markdown(track)
    assert "[Deezer]" in md
    assert "Spotify" not in md
