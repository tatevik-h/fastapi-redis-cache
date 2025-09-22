from fastapi import APIRouter, Depends
from schemas import PayloadRead


router = APIRouter()

@router.get("/{payload_id}", response_model=PayloadRead)
async def read_payload(payload_id: int):
    return {"output": "result"}