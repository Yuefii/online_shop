from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    stock: int = 0
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime | None = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True

from typing import List

class PaginatedProductResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    size: int
    pages: int
