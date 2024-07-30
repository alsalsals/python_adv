import json
from http import HTTPStatus
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, paginate, add_pagination

from models.AppStatus import AppStatus
from models.User import User


app = FastAPI()

users: list[User]


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/ping", status_code=HTTPStatus.OK)
def ping() -> dict[str, str]:
    return {"message": "pong"}


@app.get("/", status_code=HTTPStatus.OK)
def service_status() -> dict:
    return {"message": "Service is running"}


@app.get("/api/user/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    elif user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    return users[user_id - 1]


@app.get("/api/users/all", status_code=HTTPStatus.OK)
def get_users_all() -> list[User]:
    return users


@app.get("/api/users", status_code=HTTPStatus.OK, response_model=Page[User])
def get_users() -> Page[User]:
    return paginate(users)


add_pagination(app)


if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    for user in users:
        User.model_validate(user)

    uvicorn.run(app, host="localhost", port=8002)
