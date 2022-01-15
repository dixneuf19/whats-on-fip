import pytest

from whats_on_fip.models import Track
from whats_on_fip.unofficial_api import get_now_unofficial


@pytest.mark.asyncio
async def test_get_now_unofficial():
    assert Track(**get_now_unofficial().dict())


@pytest.mark.asyncio
async def test_get_now_unofficial_with_cover():
    """
    Test the assumption that when the unofficial API works, there is always a cover
    """
    assert Track(**get_now_unofficial().dict()).external_urls is not None
