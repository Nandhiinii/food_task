import time
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu import Menu
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.utils.enums import VALID_STATUS_TRANSITIONS
from app.utils.enums import OrderStatus


router = APIRouter(prefix="/api/orders", tags=["Orders"])

def simulate_status_flow(order_id: int):
    db = next(get_db())

    time.sleep(5)
    order = db.query(Order).get(order_id)
    if order:
        order.status = OrderStatus.PREPARING
        db.commit()

    time.sleep(5)
    order.status = OrderStatus.OUT_FOR_DELIVERY
    db.commit()

    time.sleep(5)
    order.status = OrderStatus.DELIVERED
    db.commit()

    db.close()

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    payload: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Cart cannot be empty")

    new_order = Order(
        customer_name=payload.customer_name,
        address=payload.address,
        phone=payload.phone,
        status=OrderStatus.RECEIVED,
        total_amount=0
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total_amount = 0

    for item in payload.items:
        menu_item = db.query(Menu).filter(Menu.id == item.menu_id).first()

        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item.menu_id} not found"
            )

        line_total = menu_item.price * item.quantity  # ✅ price × quantity
        total_amount += line_total

        order_item = OrderItem(
            order_id=new_order.id,
            menu_id=menu_item.id,
            quantity=item.quantity,
            price_at_purchase=menu_item.price,
            line_total=line_total
        )

        db.add(order_item)

    # ✅ Update order total
    new_order.total_amount = total_amount

    db.commit()
    db.refresh(new_order)

    background_tasks.add_task(simulate_status_flow, new_order.id)

    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

from typing import List

@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    return orders

@router.patch("/{order_id}/status")
def update_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    allowed_statuses = VALID_STATUS_TRANSITIONS.get(order.status, [])

    if payload.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from {order.status} to {payload.status}"
        )

    order.status = payload.status
    db.commit()
    db.refresh(order)

    return {"message": "Status updated", "status": order.status}
