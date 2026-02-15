from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin
from app.utils.enums import OrderStatus

class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)

    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.RECEIVED,
        nullable=False
    )

    total_amount = Column(Float, nullable=False, default=0)  # ✅ NEW

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
