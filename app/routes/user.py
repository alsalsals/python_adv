from http import HTTPStatus
from typing import Iterable, Optional

from fastapi import HTTPException
from app.database import users
from app.models.User import User
from fastapi import APIRouter


router = APIRouter(prefix='/api/user')


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User is not found")
    return user
