import pytest
from src.services.transformer import transform_string, transform_list


@pytest.mark.asyncio
async def test_transform_string():
    result = await transform_string("hello")
    assert result == "HELLO"


@pytest.mark.asyncio
async def test_transform_list():
    result = await transform_list(["a", "b"])
    assert  result == ["A", "B"]
