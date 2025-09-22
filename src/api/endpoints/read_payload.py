from fastapi import APIRouter, Depends
from src.api.schemas.payload import PayloadRead

from sqlalchemy.orm import Session
from sqlmodel.ext.asyncio.session import AsyncSession


from src.db.db import get_db
from src.db.payload_repository import PayloadRepository
from src.models.payload import Payload



router = APIRouter()

@router.get("/payload/{payload_id}", response_model=PayloadRead)
async def read_payload(payload_id: int, db: AsyncSession = Depends(get_db)):
    repo = PayloadRepository(db)
    result = await repo.get_by_id(payload_id)
    if result:
        return {"output": result.output}

    return {"output": "Not Found"}