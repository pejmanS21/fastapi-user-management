from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_user_management.app import app
from fastapi_user_management.models.base import Base


@pytest.fixture(scope="session")
def db_session():
    """SQLAlchemy session instance."""
    # set up
    engine = create_engine("sqlite+pysqlite:///:memory:", pool_pre_ping=True)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    yield TestSessionLocal()

    # tear down
    TestSessionLocal.close_all()


@pytest.fixture(scope="session")
def test_app() -> Generator[TestClient, None, None]:
    """FastAPI App Instance.

    Yields:
        Generator[TestClient, None, None]: generated client.
    """
    # set up
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="session")
def valid_credentials() -> dict[str, str]:
    """Correct User."""
    return {"username": "admin@gmail.com", "password": "super-secret"}


@pytest.fixture(scope="session")
def invalid_credentials() -> dict[str, str]:
    """Invalid User."""
    return {"username": "admin@gmail.com", "password": "invalidpassword"}


@pytest.fixture(scope="session")
def missing_credentials() -> dict:
    """Empty credentials."""
    return {}
