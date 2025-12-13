
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from api.db.conn import get_db
from api.dependencies import get_current_user

class ReviewCreate(BaseModel):
    product_id: int
    order_id: int
    rating: int  # 1-5
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    user_name: Optional[str] = None

router = APIRouter()

# DB Helper functions
def create_review_db(db_conn, user_id: int, review: ReviewCreate):
    db, cursor = db_conn
    
    # 1. Check if order is valid and completed
    # Using existing logic or raw query
    cursor.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (review.order_id, user_id))
    order = cursor.fetchone()
    if not order:
        raise ValueError("Order not found or not owned by user")
    
    if order['status'] != 'completed':
        raise ValueError("Can only review products from completed orders")

    # 2. Check if product is in order
    cursor.execute("SELECT * FROM order_items WHERE order_id = %s AND product_id = %s", (review.order_id, review.product_id))
    item = cursor.fetchone()
    if not item:
        raise ValueError("Product was not in this order")

    # 3. Check if already reviewed (Optional, but good practice)
    cursor.execute("SELECT id FROM reviews WHERE order_id = %s AND product_id = %s", (review.order_id, review.product_id))
    existing = cursor.fetchone()
    if existing:
        raise ValueError("You have already reviewed this product for this order")

    # 4. Insert Review
    cursor.execute(
        "INSERT INTO reviews (user_id, product_id, order_id, rating, comment) VALUES (%s, %s, %s, %s, %s)",
        (user_id, review.product_id, review.order_id, review.rating, review.comment)
    )
    review_id = cursor.lastrowid
    db.commit()
    
    # 5. Return created review
    cursor.execute("SELECT * FROM reviews WHERE id = %s", (review_id,))
    return cursor.fetchone()

def get_product_reviews_db(db_conn, product_id: int):
    db, cursor = db_conn
    cursor.execute("""
        SELECT r.*, u.full_name as user_name 
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.product_id = %s
        ORDER BY r.created_at DESC
    """, (product_id,))
    return cursor.fetchall()

# Endpoints
@router.post("/", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    try:
        new_review = create_review_db(db, current_user['id'], review)
        # Populate user_name for response
        new_review['user_name'] = current_user['full_name']
        return new_review
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int, db=Depends(get_db)):
    return get_product_reviews_db(db, product_id)
