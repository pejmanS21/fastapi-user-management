from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from mimesis import Locale, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_user_management.app import app
from fastapi_user_management.models.base import Base
from fastapi_user_management.models.role import RoleNames
from fastapi_user_management.models.user import UserStatusValues


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


@pytest.fixture(scope="session")
def new_user_data() -> dict[str, Any]:
    """Fixture for a user data used in creating a new user."""
    person = Person(Locale.EN)
    return {
        "fullname": person.full_name(),
        "username": person.email(),
        "password": person.password(),
        "status": UserStatusValues.ACTIVE,
        "roles": [{"name": RoleNames.USER}],
    }


@pytest.fixture(scope="session")
def existing_user_data() -> dict[str, Any]:
    """Fixture for an existing user data."""
    person = Person(Locale.EN)
    return {
        "fullname": person.full_name(),
        "username": person.email(unique=True),
        "password": person.password(),
        "status": UserStatusValues.PENDING,
        "roles": [{"name": RoleNames.USER}],
    }
