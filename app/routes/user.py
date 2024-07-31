from http import HTTPStatus

from fastapi import HTTPException
from app.database import users_db
from app.models.User import User
from fastapi import APIRouter


router = APIRouter(prefix='/api/user')


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id > len(users_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    elif user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    return users_db[user_id - 1]
