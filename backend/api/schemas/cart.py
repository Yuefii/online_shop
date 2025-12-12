from pydantic import BaseModel
from typing import List, Optional
from api.schemas.product import ProductResponse

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    total_price: float
