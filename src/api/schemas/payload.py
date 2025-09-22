from pydantic import BaseModel
from typing import List

class PayloadCreate(BaseModel):
    list_1: List[str]
    list_2: List[str]

class PayloadRead(BaseModel):
    output: str
