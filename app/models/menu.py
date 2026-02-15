from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base
from app.models.base import TimestampMixin

class Menu(Base, TimestampMixin):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    image_url = Column(String(255))
