import pytest
from httpx import AsyncClient
from src.main import app


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac