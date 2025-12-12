from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from api.schemas.category import CategoryCreate, CategoryResponse
from api.db.categories import get_all_categories, get_category_by_id, create_category
from api.db.conn import get_db
from api.core.limiter import limiter

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
@limiter.limit("5/minute")
def list_categories(request: Request, db=Depends(get_db)):
    return get_all_categories(db)

@router.post("/", response_model=CategoryResponse)
@limiter.limit("5/minute")
def create_new_category(category: CategoryCreate, request: Request, db=Depends(get_db)):
    category_id = create_category(db, category.name, category.slug)
    return get_category_by_id(db, category_id)

@router.get("/{category_id}", response_model=CategoryResponse)
@limiter.limit("5/minute")
def get_category(category_id: int, request: Request, db=Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
