import os
from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set to connect to PostgreSQL.")

    return create_engine(database_url, pool_pre_ping=True)


def get_db_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session
