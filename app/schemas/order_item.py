from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    id: int
    menu_id: int
    quantity: int
    price_at_purchase: float
    line_total: float  # ✅ NEW

    class Config:
        from_attributes = True

