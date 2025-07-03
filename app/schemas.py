from pydantic import BaseModel, Field, validator
from typing import Dict, List, Literal

Category = Literal["Broken", "Needs Improvement", "Ideal",
                   "Gold Standard", "No Match"]

# ---------- Incoming ---------- #
class ItemIn(BaseModel):
    id: int
    question: str
    criteria: Dict[str, str]          # only the four real categories
    answer: str = Field(..., example="We close audits 120 days after year‑end")

    @validator("criteria")
    def at_least_four(cls, v):
        if len(v) < 4:
            raise ValueError("criteria needs 4 categories (Broken→Gold Standard)")
        return v


class RequestBody(BaseModel):
    items: List[ItemIn]


# ---------- Outgoing ---------- #
class ItemOut(BaseModel):
    id: int
    question: str
    picked_category: Category
    confidence: float                 # 0‑1


class ResponseBody(BaseModel):
    results: List[ItemOut]
