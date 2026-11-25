import pytest
from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import sessionmaker

from entity.base import Base

SERVER_URL = "postgresql+psycopg://pguser:example@localhost:5432"
DB_NAME = "database_test"

def db_prep():
    engine = create_engine(f"{SERVER_URL}/database", isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
    engine.dispose()

@pytest.fixture(scope="session", autouse=True)
def db_session():
    db_prep()
    engine = create_engine(f"{SERVER_URL}/{DB_NAME}")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()