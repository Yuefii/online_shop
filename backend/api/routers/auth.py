from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas.user import UserCreate
from api.db.repository import get_user_by_email, create_user
from api.db.conn import get_db
from api.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from api.core.limiter import limiter
from api.core.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi import Request, Header, Response


router = APIRouter()


@router.post("/register")
@limiter.limit("5/minute")
def register(user: UserCreate, request: Request, db: tuple = Depends(get_db)):
    existed = get_user_by_email(db, user.email)
    if existed:
        raise HTTPException(400, "Email already registered")
    create_user(db, user.email, hash_password(user.password), user.full_name)
    return {"message": "User created"}


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, response: Response, form: OAuth2PasswordRequestForm = Depends(), db: tuple = Depends(get_db)):
    user = get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(400, "Invalid credentials")
    
    access_token = create_access_token({"sub": user["email"]})
    refresh_token = create_refresh_token({"sub": user["email"]})
    
    # Set HttpOnly Cookies
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True, 
        max_age=60 * 60, # 1 hour
        samesite="lax",
        secure=False # Set to True in production with HTTPS
    )
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True, 
        max_age=60 * 60 * 24 * 7, # 7 days
        samesite="lax",
        secure=False
    )
    
    return {"message": "Login successful"}


@router.post("/refresh")
def refresh_token(response: Response, request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
         raise HTTPException(401, "Refresh token missing")
         
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
             raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
        
    new_access_token = create_access_token({"sub": email})
    
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {new_access_token}", 
        httponly=True, 
        max_age=60 * 60,
        samesite="lax",
        secure=False
    )
    
    return {"message": "Token refreshed"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}