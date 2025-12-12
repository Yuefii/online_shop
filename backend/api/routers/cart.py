from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from api.db.conn import get_db
from api.dependencies import get_current_user
from api.schemas.cart import CartResponse, CartItemCreate
from api.db import cart as cart_db

router = APIRouter()

@router.get("/", response_model=CartResponse)
def get_my_cart(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    user_id = current_user['id']
    return cart_db.get_cart_by_user_id(db, user_id)

@router.post("/items", response_model=CartResponse)
def add_item_to_cart(
    item: CartItemCreate, 
    current_user: dict = Depends(get_current_user), 
    db=Depends(get_db)
):
    user_id = current_user['id']
    return cart_db.add_to_cart(db, user_id, item.product_id, item.quantity)

@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_item_from_cart(
    item_id: int, 
    current_user: dict = Depends(get_current_user), 
    db=Depends(get_db)
):
    user_id = current_user['id']
    return cart_db.remove_from_cart(db, user_id, item_id)
