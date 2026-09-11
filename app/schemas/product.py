from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    category_id: int
    current_price: float
    original_price: float | None = None
    ml_item_id: str | None = None
    url: str | None = None
    image_url: str | None = None
    rating: float | None = None
    review_count: int = 0
    sold_quantity: int = 0
    stock_quantity: int | None = None


class ProductResponse(BaseModel):
    id: int
    title: str
    category_id: int
    current_price: float
    original_price: float | None
    ml_item_id: str | None
    url: str | None
    image_url: str | None
    rating: float | None
    review_count: int
    sold_quantity: int
    stock_quantity: int | None
    active: bool

    model_config = {
        "from_attributes": True
    }