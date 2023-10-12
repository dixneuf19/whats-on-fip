import pytest

from whats_on_fip.models import Track
from whats_on_fip.radio_fiftyfifty import Radio5050


@pytest.mark.asyncio
async def test_get_current_track_remote():
    radio = Radio5050()
    assert Track(**radio.get_current_track().model_dump())
