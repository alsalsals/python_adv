import json
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.models.User import User
from app.routes import status, user, users
from database import users_db

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
app.include_router(user.router)


add_pagination(app)


if __name__ == "__main__":
    with open("../users.json") as f:
        users_db.extend(json.load(f))

    for user in users_db:
        User.model_validate(user)

    uvicorn.run(app, host="localhost", port=8002)
