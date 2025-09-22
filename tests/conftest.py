import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock
from src.main import app
from src.services import cache_service


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def mock_cache(monkeypatch):
    monkeypatch.setattr(cache_service, "get_cache", AsyncMock(return_value=None))
    monkeypatch.setattr(cache_service, "set_cache", AsyncMock(return_value=None))
