import asyncio


async def transform_string(s: str) -> str:
    """
    Simulate external service transformation asynchronously.
    Converts string to uppercase after a short delay.
    """
    await asyncio.sleep(0.1)
    return s.upper()


async def transform_list(strings: list[str]) -> list[str]:
    """
    Transform a list of string asynchronously.
    """
    tasks = [transform_string(s) for s in strings]
    return await asyncio.gather(*tasks)