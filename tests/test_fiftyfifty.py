import pytest

from whats_on_fip.models import Track
from whats_on_fip.radio_fiftyfifty import get_current_song


@pytest.mark.asyncio
async def test_get_current_song_remote():
    assert Track(**get_current_song().dict())
