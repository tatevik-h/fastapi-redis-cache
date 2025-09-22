import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from src.main import app

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
def mock_cache():
    with patch("src.services.cache_service.get_cache", new_callable=AsyncMock) as get_mock, \
         patch("src.services.cache_service.set_cache", new_callable=AsyncMock) as set_mock:
        get_mock.return_value = None
        set_mock.return_value = None
        yield