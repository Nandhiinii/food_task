from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MenuBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    image_url: Optional[str]


class MenuCreate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
