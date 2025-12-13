from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from api.schemas.category import CategoryCreate, CategoryResponse, PaginatedCategoryResponse
from api.db.categories import get_all_categories, get_category_by_id, create_category, update_category, delete_category, count_categories
from api.db.conn import get_db
from api.core.limiter import limiter

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def list_categories(request: Request, db=Depends(get_db), q: str = None):
    return get_all_categories(db, search_query=q)

@router.get("/paginated", response_model=PaginatedCategoryResponse)
def list_categories_paginated(
    request: Request, 
    db=Depends(get_db),
    q: str = None,
    page: int = 1,
    size: int = 10
):
    offset = (page - 1) * size
    items = get_all_categories(db, search_query=q, limit=size, offset=offset)
    total = count_categories(db, search_query=q)
    
    import math
    pages = math.ceil(total / size) if size > 0 else 0
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

from api.dependencies import get_current_admin_user

@router.post("/", response_model=CategoryResponse)
@limiter.limit("20/minute")
def create_new_category(
    category: CategoryCreate, 
    request: Request, 
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    category_id = create_category(db, category.name, category.slug)
    return get_category_by_id(db, category_id)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, request: Request, db=Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
@limiter.limit("20/minute")
def update_existing_category(
    category_id: int, 
    category: CategoryCreate, 
    request: Request, 
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    existing_category = get_category_by_id(db, category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_category(db, category_id, name=category.name, slug=category.slug)
    return get_category_by_id(db, category_id)

@router.delete("/{category_id}")
@limiter.limit("20/minute")
def delete_existing_category(
    category_id: int, 
    request: Request, 
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    existing_category = get_category_by_id(db, category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    delete_category(db, category_id)
    return {"message": "Category deleted successfully"}
