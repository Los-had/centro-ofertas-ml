from datetime import datetime

from pydantic import BaseModel


class PriceHistoryCreate(BaseModel):
    price: float


class PriceHistoryResponse(BaseModel):
    id: int
    product_id: int
    price: float
    recorded_at: datetime

    model_config = {
        "from_attributes": True
    }