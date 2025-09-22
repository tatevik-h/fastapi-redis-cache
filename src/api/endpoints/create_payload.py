from fastapi import APIRouter, Depends
from src.api.schemas.payload import PayloadCreate, PayloadGet

from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.payload_service import generate_payload
from src.db.db import get_db

router = APIRouter()

@router.post("/payload/", response_model=PayloadGet)
async def create_payload(payload_in: PayloadCreate, session: AsyncSession = Depends(get_db)):
    payload = await generate_payload(payload_in.list_1, payload_in.list_2, session)
    return {"id": payload.id}
