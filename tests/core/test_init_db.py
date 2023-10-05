# test_database.py

import pytest

from fastapi_user_management import crud
from fastapi_user_management.config import SETTINGS
from fastapi_user_management.core.database import get_db
from fastapi_user_management.core.init_db import init_db


@pytest.mark.integration()
def test_init_db_admin_exists() -> None:
    """Test init db if user exist."""
    # Arrange
    db = next(get_db())

    try:
        # Act
        init_db(db)

        # Assert
        admin_user = crud.user.get_by_username(db, username=SETTINGS.ADMIN_EMAIL)
        assert admin_user is not None
        assert admin_user.username == SETTINGS.ADMIN_EMAIL
        # Add more assertions based on your specific requirements
    finally:
        # Clean up
        db.close()


@pytest.mark.integration()
def test_init_db_create_admin() -> None:
    """Test init db if user not exist."""
    # Arrange
    db = next(get_db())
    crud.user.remove_by_username(db=db, username=SETTINGS.ADMIN_EMAIL)
    try:
        # Act
        init_db(db)

        # Assert
        admin_user = crud.user.get_by_username(db, username=SETTINGS.ADMIN_EMAIL)
        assert admin_user is not None
        assert admin_user.username == SETTINGS.ADMIN_EMAIL
        # Add more assertions based on your specific requirements
    finally:
        # Clean up
        db.close()
