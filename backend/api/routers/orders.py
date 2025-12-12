from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from api.db.conn import get_db
from api.dependencies import get_current_user
from api.schemas.order import OrderCreate, OrderResponse
from api.db import orders as orders_db

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def create_order(
    order_in: OrderCreate,
    current_user: dict = Depends(get_current_user), 
    db=Depends(get_db)
):
    user_id = current_user['id']
    try:
        return orders_db.create_order(db, user_id, order_in.shipping_address)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[OrderResponse])
def list_my_orders(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    user_id = current_user['id']
    return orders_db.get_orders_by_user(db, user_id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    user_id = current_user['id']
    order = orders_db.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    return order
