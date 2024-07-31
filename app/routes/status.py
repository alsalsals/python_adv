from http import HTTPStatus
from fastapi import APIRouter
from app.database import users_db
from app.models.AppStatus import AppStatus


router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users_db))


@router.get("/ping", status_code=HTTPStatus.OK)
def ping() -> dict[str, str]:
    return {"message": "pong"}


@router.get("/", status_code=HTTPStatus.OK)
def service_status() -> dict:
    return {"message": "Service is running"}
