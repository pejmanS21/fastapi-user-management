"""DataBase Session maker."""
from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_user_management.config import SETTINGS

engine = create_engine(
    SETTINGS.DATABASE_URI, pool_pre_ping=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db() -> Generator[Any, Any, None]:
    """Function to inject database as dependency via fastapi functionalities.

    Yields:
        Generator[Any, Any, None]: database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
