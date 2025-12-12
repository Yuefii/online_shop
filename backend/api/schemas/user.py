from pydantic import BaseModel, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True