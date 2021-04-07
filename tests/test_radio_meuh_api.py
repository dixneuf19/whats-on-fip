import pytest

from whatsonfip.radio_meuh_api import get_current_song
from whatsonfip.models import Track


@pytest.mark.asyncio
async def test_get_current_song():
    assert Track(**get_current_song().dict())
