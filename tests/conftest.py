import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.db.db import get_db

@pytest.fixture(autouse=True)
def mock_cache():
    with patch("src.services.payload_service.get_cache", new_callable=AsyncMock) as get_mock, \
         patch("src.services.payload_service.set_cache", new_callable=AsyncMock) as set_mock:
        get_mock.return_value = None
        set_mock.return_value = None
        yield

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        yield s

@pytest_asyncio.fixture
async def client(session: AsyncSession):
    app.dependency_overrides[get_db] = lambda: session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
