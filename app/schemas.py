from pydantic import BaseModel, Field, validator
from typing import Dict, List

# ---------- Incoming ---------- #
class ItemIn(BaseModel):
    id: int
    question: str
    criteria: Dict[str, str]
    answer: str = Field(..., example="We close audits 120 days after year‑end")

    @validator("criteria")
    def at_least_two(cls, v):
        if len(v) < 2:
            raise ValueError("criteria needs ≥2 categories")
        return v


class RequestBody(BaseModel):
    items: List[ItemIn]


# ---------- Outgoing ---------- #
class ItemOut(BaseModel):
    id: int
    question: str
    picked_category: str
    confidence: float          # 0‑1


class ResponseBody(BaseModel):
    results: List[ItemOut]
