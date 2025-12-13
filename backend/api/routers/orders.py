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

from api.dependencies import get_current_admin_user
from pydantic import BaseModel

class OrderStatusUpdate(BaseModel):
    status: str

@router.get("/admin/all", response_model=List[OrderResponse])
def list_all_orders(
    q: str = None,
    admin: dict = Depends(get_current_admin_user), 
    db=Depends(get_db)
):
    return orders_db.get_all_orders(db, search_query=q)

@router.get("/admin/stats")
def get_stats(
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    return orders_db.get_order_stats(db)

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int, 
    status_update: OrderStatusUpdate,
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    order = orders_db.update_order_status(db, order_id, status_update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{order_id}/pay", response_model=OrderResponse)
def pay_order(order_id: int, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 1. Get order check ownership
    order = orders_db.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 2. Check status
    if order['status'] != 'pending':
        raise HTTPException(status_code=400, detail="Order is already paid or cancelled")
        
    # 3. Simulate payment success -> update status
    # In real world, here we would verify with Stripe/Midtrans
    return orders_db.update_order_status(db, order_id, 'processing')

@router.post("/{order_id}/receive", response_model=OrderResponse)
def receive_order(order_id: int, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 1. Get order check ownership
    order = orders_db.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 2. Check status
    if order['status'] != 'shipped':
        raise HTTPException(status_code=400, detail="Order must be shipped before it can be received")
        
    # 3. Update status to completed
    return orders_db.update_order_status(db, order_id, 'completed')

@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: int, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 1. Get order
    order = orders_db.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    is_admin = current_user.get('role') == 'admin'
    is_owner = order['user_id'] == current_user['id']
    
    if not is_admin and not is_owner:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 2. Check status based on role
    allowed = False
    if is_admin:
        if order['status'] in ['pending', 'processing']:
            allowed = True
    elif is_owner:
        if order['status'] == 'pending':
            allowed = True
            
    if not allowed:
        raise HTTPException(status_code=400, detail=f"Cannot cancel order in status '{order['status']}'")
        
    # 3. Update status to cancelled
    return orders_db.update_order_status(db, order_id, 'cancelled')
