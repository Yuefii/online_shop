from pydantic import BaseModel
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime | None = None

    class Config:
        from_attributes = True

from typing import List

class PaginatedCategoryResponse(BaseModel):
    items: List[CategoryResponse]
    total: int
    page: int
    size: int
    pages: int
