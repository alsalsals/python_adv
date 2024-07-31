from typing import Iterable

from sqlmodel import Session, select
from typing_extensions import Optional

from .engine import engine
from ..models import User


def get_user(user_id: int) -> Optional[User]:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> Iterable[User]:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


