from fastapi import APIRouter, Depends
from api.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    if "password" in user:
        del user["password"]
    return user

