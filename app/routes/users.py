from http import HTTPStatus
from typing import Iterable

from fastapi import HTTPException
from fastapi_pagination import Page, paginate
from app.database import users
from app.models.User import User
from fastapi import APIRouter


router = APIRouter(prefix='/api/users')


@router.get("/all", status_code=HTTPStatus.OK)
def get_users_all() -> Iterable[User]:
    return users.get_users()


@router.get("/", status_code=HTTPStatus.OK, response_model=Page[User])
def get_users() -> Iterable[User]:
    return paginate(users.get_users())
