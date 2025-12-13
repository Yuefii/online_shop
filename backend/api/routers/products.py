from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from api.schemas.product import ProductCreate, ProductResponse
from api.db.products import get_all_products, get_product_by_id, create_product, update_product, delete_product
from api.db.conn import get_db
from api.core.limiter import limiter

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def list_products(
    request: Request, 
    db=Depends(get_db),
    q: str = None,
    min_price: float = None,
    max_price: float = None,
    category_id: int = None
):
    return get_all_products(db, search_query=q, min_price=min_price, max_price=max_price, category_id=category_id)

from api.dependencies import get_current_admin_user

@router.post("/", response_model=ProductResponse)
@limiter.limit("20/minute")
def create_new_product(
    product: ProductCreate, 
    request: Request, 
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    product_id = create_product(
        db, 
        name=product.name, 
        price=product.price, 
        category_id=product.category_id,
        description=product.description,
        image_url=product.image_url,
        stock=product.stock
    )
    return get_product_by_id(db, product_id)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, request: Request, db=Depends(get_db)):
    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
@limiter.limit("20/minute")
def update_existing_product(
    product_id: int, 
    product: ProductCreate, 
    request: Request, 
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    existing_product = get_product_by_id(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_product(
        db, 
        product_id, 
        name=product.name, 
        price=product.price, 
        category_id=product.category_id, 
        description=product.description, 
        image_url=product.image_url, 
        stock=product.stock
    )
    
    return get_product_by_id(db, product_id)

@router.delete("/{product_id}")
@limiter.limit("20/minute")
def delete_existing_product(
    product_id: int, 
    request: Request, 
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    existing_product = get_product_by_id(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    delete_product(db, product_id)
    
    return {"message": "Product deleted successfully"}
