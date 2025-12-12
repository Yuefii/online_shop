from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas.user import UserCreate
from api.db.repository import get_user_by_email, create_user
from api.db.conn import get_db
from api.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from api.core.limiter import limiter
from api.core.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi import Request, Header


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
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: tuple = Depends(get_db)):
    user = get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(400, "Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    refresh_token = create_refresh_token({"sub": user["email"]})
    return {"access_token": token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(token: str = Header(..., alias="x-refresh-token")):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
             raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
        
    access_token = create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}