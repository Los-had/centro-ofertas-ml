from datetime import datetime

from pydantic import BaseModel


class DealResponse(BaseModel):
    id: int
    product_id: int
    score: float
    discount_percent: float
    status: str
    reason: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }