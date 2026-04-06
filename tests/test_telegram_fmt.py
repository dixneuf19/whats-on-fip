from whats_on_fip.models import FEELGOOD_RADIO, MEUH_RADIO, Track
from whats_on_fip.telegram.fmt import track_to_markdown


def test_track_to_markdown_full():
    track = Track(
        title="The Logical Song",
        artist="Supertramp",
        album="Breakfast In America",
        year=1979,
    )
    md = track_to_markdown(track)
    assert "*Live on [FIP](https://www.fip.fr) :*" in md
    assert "*The Logical Song*" in md
    assert "_Supertramp_" in md
    assert "Breakfast In America" in md
    assert "1979" in md


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


def test_track_to_markdown_only_year():
    track = Track(title="Song", artist="Artist", year=2020)
    md = track_to_markdown(track)
    assert "2020" in md
    assert r"\-" not in md


def test_track_to_markdown_only_album():
    track = Track(title="Song", artist="Artist", album="Album")
    md = track_to_markdown(track)
    assert "Album" in md
    assert r"\-" not in md
