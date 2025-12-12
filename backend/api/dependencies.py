from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.core.config import SECRET_KEY, ALGORITHM
from api.db.conn import get_db
from api.db.repository import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: tuple = Depends(get_db)):
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



