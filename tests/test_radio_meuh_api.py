import pytest

from whatsonfip.models import Track
from whatsonfip.radio_meuh_api import get_current_song


@pytest.mark.asyncio
async def test_get_current_song():
    assert Track(**get_current_song().dict())
