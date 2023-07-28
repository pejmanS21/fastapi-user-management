from typing import TypedDict

import pytest
from mimesis import Person
from mimesis.locales import Locale
from sqlalchemy.orm import Session

from fastapi_user_management import crud
from fastapi_user_management.errors.exceptions import PasswordMatchError
from fastapi_user_management.schemas.role import RoleBase
from fastapi_user_management.schemas.user import UserCreate, UserUpdate
from fastapi_user_management.tools.encryption import verify_password


class SampleUserStub(TypedDict):
    """Stub for create dictionary."""

    fullname: str
    username: str
    password: str
    roles: list[RoleBase]


@pytest.fixture(scope="function")
def sample_user() -> SampleUserStub:
    """Generate new random info for user.

    Returns:
        SampleUserStub: new info.
    """
    person = Person(Locale.EN)
    new_user: SampleUserStub = {
        "fullname": person.full_name(),
        "username": person.email(unique=True),
        "password": person.password(length=18),
        "roles": [RoleBase(name="user")],
    }
    return new_user


def test_create_new_user_with_valid_input_data(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Test to create new user."""
    user = crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    assert user is not None
    assert user.fullname == sample_user["fullname"]
    assert user.username == sample_user["username"]
    assert user.roles[0].name == "user"


def test_update_user_info_with_invalid_input_data(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Tests that user info can not be updated with invalid input data."""
    user = crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    updated_user_data = {
        "new_password": "newpassword123",
        "new_password_confirm": "no-password",
    }
    with pytest.raises(PasswordMatchError):
        crud.user.update(
            db=db_session, db_obj=user, obj_in=UserUpdate(**updated_user_data)
        )


def test_update_user_info_with_valid_input_data_object(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Tests that user info can be updated with valid input data is pydantic object."""
    user = crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    updated_user_data = {
        "new_password": "newpassword123",
        "new_password_confirm": "newpassword123",
    }
    updated_user = crud.user.update(
        db=db_session, db_obj=user, obj_in=UserUpdate(**updated_user_data)
    )
    assert updated_user is not None
    assert verify_password(
        plain_password="newpassword123", hashed_password=updated_user.password
    )


def test_update_user_info_with_valid_input_data_dict(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Tests that user info can be updated with valid input data as dict."""
    user = crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    updated_user_data = {
        "new_password": "newpassword123",
        "new_password_confirm": "newpassword123",
    }
    updated_user = crud.user.update(
        db=db_session, db_obj=user, obj_in=updated_user_data
    )
    assert updated_user is not None
    assert verify_password(
        plain_password="newpassword123", hashed_password=updated_user.password
    )


def test_authenticate_user_with_invalid_credentials(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Tests that a user can not be authenticated with invalid credentials."""
    crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    authenticated_user_1 = crud.user.authenticate(
        db=db_session,
        username="username",
        password="password",
    )
    authenticated_user_2 = crud.user.authenticate(
        db=db_session,
        username=sample_user["username"],
        password="password",
    )
    assert authenticated_user_1 is None
    assert authenticated_user_2 is None


def test_authenticate_user_with_valid_credentials(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Tests that a user can be authenticated with valid credentials."""
    crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    authenticated_user = crud.user.authenticate(
        db=db_session,
        username=sample_user["username"],
        password=sample_user["password"],
    )
    assert authenticated_user is not None
    assert authenticated_user.username == sample_user["username"]


def test_get_user_status(db_session: Session, sample_user: SampleUserStub) -> None:
    """Tests that for `is_active` method in `crud.user`."""
    new_user = crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    assert not crud.user.is_active(user=new_user)


def test_get_user_record_role(db_session: Session, sample_user: SampleUserStub) -> None:
    """Tests that for `is_admin` in `crud.user`."""
    sample_user["roles"].append(RoleBase(name="admin"))
    new_user = crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    assert crud.user.is_admin(db=db_session, db_obj=new_user)


def test_remove_user_by_username_with_valid_input_data(
    db_session: Session, sample_user: SampleUserStub
) -> None:
    """Tests that a user can be removed by username with valid input data."""
    crud.user.create(
        db=db_session,
        obj_in=UserCreate(**sample_user),
    )
    removed_user = crud.user.remove_by_username(
        db=db_session, username=sample_user["username"]
    )
    assert removed_user is not None
    assert removed_user.username == sample_user["username"]


def test_create_new_user_with_empty_input_data(db_session: Session) -> None:
    """Tests that a new user cannot be created with empty input data."""
    user_data = {}
    with pytest.raises(Exception):  # noqa: B017
        crud.user.create(db=db_session, obj_in=UserCreate(user_data))


def test_create_new_user_with_invalid_email_format(db_session: Session) -> None:
    """Tests that a new user cannot be created with invalid email format."""
    user_data = {
        "fullname": "John Doe",
        "username": "johndoe",
        "password": "password123",
        "roles": [RoleBase(name="user")],
    }
    with pytest.raises(Exception):  # noqa: B017
        crud.user.create(db=db_session, obj_in=UserCreate(**user_data))
