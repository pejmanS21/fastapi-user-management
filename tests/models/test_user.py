from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from fastapi_user_management.models.user import UserModel, UserStatusValues


@pytest.fixture(scope="module")
def user_info() -> UserModel:
    """Generate new unique user."""
    uid = uuid4().hex
    user = UserModel(
        fullname=f"John Doe {uid}",
        username=uid + "@mail.com",
        password="password",
        created_at=datetime.now(),
        status=UserStatusValues.PENDING,
    )
    return user


@pytest.mark.unit()
def test_user_model_invalid_email():
    """Test to catch `ValueError` with invalid email."""
    with pytest.raises(ValueError):
        UserModel(
            fullname="John Doe",
            username="invalid_email",
            password="password",
            created_at=datetime.now(),
            status=UserStatusValues.PENDING,
        )


@pytest.mark.unit()
def test_user_model_valid_email():
    """Test Database object creation correctly."""
    user = UserModel(
        fullname="John Doe",
        username="valid_email@gmail.com",
        password="password",
        created_at=datetime.now(),
        status=UserStatusValues.PENDING,
    )
    assert isinstance(user.fullname, str)
    assert isinstance(user.username, str)
    assert isinstance(user.password, str)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.status, UserStatusValues)
    assert user.status is UserStatusValues.PENDING


@pytest.mark.integration()
def test_user_model(db_session: Session, user_info: UserModel):
    """Integration test to commit user to database & check its values."""
    user = user_info

    db_session.add(user)
    db_session.commit()

    # Retrieve the user from the database
    stored_user = db_session.query(UserModel).filter_by(fullname=user.fullname).first()

    # Assert that the stored user matches the created user
    assert stored_user is not None
    assert stored_user.fullname == user.fullname
    assert stored_user.username == user.username
    assert stored_user.password == user.password
    assert isinstance(stored_user.status, UserStatusValues)
    assert stored_user.status == user.status
