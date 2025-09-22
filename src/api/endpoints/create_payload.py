from fastapi import APIRouter
from schemas import PayloadCreate, PayloadRead

router = APIRouter()

@router.post("/", response_model=PayloadRead)
async def create_payload(payload_in: PayloadCreate):
    # TO DO generate payload
    return {"out_put": payload_in}