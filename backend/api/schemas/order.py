from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int]
    quantity: int
    price_at_purchase: float
    product_name: str # Added for convenience

class OrderCreate(BaseModel):
    shipping_address: str

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    shipping_address: str
    created_at: datetime
    items: List[OrderItemResponse] = []
