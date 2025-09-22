from fastapi import APIRouter, Depends
from src.api.schemas.payload import PayloadRead

from sqlalchemy.orm import Session

from src.db.db import get_db


router = APIRouter()

@router.get("/{payload_id}", response_model=PayloadRead)
async def read_payload(payload_id: int, db: Session = Depends(get_db)):
    async for s in session:
        result = await s.get(PayloadRead, payload_id)
        if result:
            return {"output": result.output}

    return {"output": "Not Found"}