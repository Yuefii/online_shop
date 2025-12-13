from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.core.config import SECRET_KEY, ALGORITHM
from api.db.conn import get_db
from api.db.repository import get_user_by_email

from fastapi import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: tuple = Depends(get_db)):
    # Try getting token from cookie if not in header
    if not token:
        cookie_authorization = request.cookies.get("access_token")
        if cookie_authorization:
            # Clean up "Bearer " prefix if present in cookie (not typical but I set it that way in auth.py)
            scheme, _, param = cookie_authorization.partition(" ")
            if scheme.lower() == "bearer":
                token = param
            else:
                token = cookie_authorization
    
    if not token:
        raise HTTPException(401, "Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(401, "Invalid token")
        
        user = get_user_by_email(db, email)
        if user is None:
            raise HTTPException(401, "User not found")
            
        return user
    except JWTError:
        raise HTTPException(401, "Invalid token")

def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user



