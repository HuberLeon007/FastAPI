import os
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

# echo SQL for debugging; can be disabled in production
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    """FastAPI dependency that yields a SQLModel Session"""
    with Session(engine) as session:
        yield session
