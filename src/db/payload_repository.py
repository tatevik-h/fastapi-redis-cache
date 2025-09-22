from typing import Optional

from src.models.payload import Payload
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession


class PayloadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, payload: Payload) -> Payload:
        self.session.add(payload)
        await self.session.commit()
        await self.session.refresh(payload)
        return payload

    async def get_by_id(self, payload_id: int) -> Optional[Payload]:
        result = await self.session.get(Payload, payload_id)
        return result

    async def get_by_lists(self, list_1: str, list_2: str) -> Optional[Payload]:
        q = select(Payload).where(Payload.list_1 == list_1, Payload.list_2 == list_2)
        result = await self.session.execute(q)
        return result.scalar_one_or_none()
