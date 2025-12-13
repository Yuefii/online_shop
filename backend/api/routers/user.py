from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_current_user
from api.db.conn import get_db

router = APIRouter()


@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    if "password" in user:
        del user["password"]
    return user


from typing import List
from pydantic import BaseModel
from api.dependencies import get_current_admin_user
from api.db.repository import get_all_users, update_user_role

class UserRoleUpdate(BaseModel):
    role: str

@router.get("/", response_model=List[dict])
def list_users(
    q: str = None,
    admin: dict = Depends(get_current_admin_user), 
    db=Depends(get_db)
):
    """List all users (Admin only)"""
    return get_all_users(db, search_query=q)

@router.put("/{user_id}/role")
def change_user_role(
    user_id: int, 
    role_update: UserRoleUpdate,
    admin: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    """Change user role (Admin only)"""
    success = update_user_role(db, user_id, role_update.role)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Role updated successfully"}
