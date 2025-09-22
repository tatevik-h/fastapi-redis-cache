from src.db.payload_repository import PayloadRepository
from src.models import Payload
from src.services.transformer import transform_list
from src.services.cache_service import get_cache, set_cache
from sqlmodel.ext.asyncio.session import AsyncSession


async def generate_payload(list_1, list_2, session: AsyncSession):
    key = f"{list_1}-{list_2}"

    cached = await get_cache(key)
    if cached:
        return cached


    repo = PayloadRepository(session)
    existing = await repo.get_by_lists(str(list_1), str(list_2))
    if existing:
        return existing

    transformed_1 = await transform_list(list_1)
    transformed_2 = await  transform_list(list_2)

    output = ",".join(val for pair in zip(transformed_1, transformed_2) for val in pair)

    payload = Payload(list_1=str(list_1), list_2=str(list_2), output=output)

    await set_cache(key, {"output": payload.output})

    return payload
