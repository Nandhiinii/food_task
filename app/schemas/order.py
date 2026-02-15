from pydantic import BaseModel, Field, constr
from typing import List
from datetime import datetime
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from app.utils.enums import OrderStatus


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2)
    address: str = Field(..., min_length=5)
    phone: constr(pattern=r'^\d{10}$')
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    address: str
    phone: str
    status: OrderStatus
    total_amount: float  # ✅ NEW
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True



class OrderStatusUpdate(BaseModel):
    status: OrderStatus
