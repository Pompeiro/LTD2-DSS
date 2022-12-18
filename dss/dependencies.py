import typing as T

from sqlmodel import Session

from .database import engine


def get_session() -> T.Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
