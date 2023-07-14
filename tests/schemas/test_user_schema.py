from typing import TypedDict

import pytest

from fastapi_user_management.models.role import RoleNames
from fastapi_user_management.models.user import UserStatusValues
from fastapi_user_management.schemas.role import RoleBase
from fastapi_user_management.schemas.user import (
    BaseUserCreate,
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
)


class SampleUserInfo(TypedDict):
    """Type hint dictionary for fixture."""

    fullname: str
    username: str
    status: UserStatusValues
    roles: list[RoleBase]
    password: str


@pytest.fixture()
def sample_user_information() -> SampleUserInfo:
    """Fixture that returns a sample user information dictionary."""
    return {
        "fullname": "John Doe",
        "username": "johndoe@mail.com",
        "status": UserStatusValues.ACTIVE,
        "roles": [RoleBase(name=RoleNames.USER)],
        "password": "password",
    }


@pytest.mark.unit()
def test_user_base_model_schema(sample_user_information: SampleUserInfo) -> None:
    """Test the UserBase schema."""
    user_info: SampleUserInfo = sample_user_information
    user = UserBase(
        fullname=user_info["fullname"],
        username=user_info["username"],
        status=user_info["status"],
        roles=user_info["roles"],
    )

    assert isinstance(user.fullname, str)
    assert isinstance(user.username, str)
    assert isinstance(user.status, UserStatusValues)
    assert isinstance(user.roles, list)
    assert isinstance(user.roles[0], RoleBase)
    assert user.username == sample_user_information["username"]


@pytest.mark.unit()
def test_base_user_create_schema(sample_user_information: SampleUserInfo) -> None:
    """Test the BaseUserCreate schema."""
    user_info: SampleUserInfo = sample_user_information
    new_user = BaseUserCreate(
        fullname=user_info["fullname"],
        username=user_info["username"],
        roles=user_info["roles"],
    )
    assert isinstance(new_user.fullname, str)
    assert isinstance(new_user.username, str)
    assert isinstance(new_user.roles, list)
    assert isinstance(new_user.roles[0], RoleBase)


@pytest.mark.unit()
def test_user_create_schema(sample_user_information: SampleUserInfo) -> None:
    """Test the UserCreate schema."""
    user_info: SampleUserInfo = sample_user_information
    new_user = UserCreate(
        fullname=user_info["fullname"],
        username=user_info["username"],
        roles=user_info["roles"],
        password=user_info["password"],
    )
    assert isinstance(new_user.fullname, str)
    assert isinstance(new_user.username, str)
    assert isinstance(new_user.roles, list)
    assert isinstance(new_user.roles[0], RoleBase)
    assert isinstance(new_user.password, str)
    assert new_user.password == "password"


@pytest.mark.unit()
def test_user_login_schema(sample_user_information: SampleUserInfo) -> None:
    """Test the UserLogin schema."""
    user_info: SampleUserInfo = sample_user_information
    user = UserLogin(
        username=user_info["username"],
        password=user_info["password"],
    )
    assert isinstance(user.username, str)
    assert isinstance(user.password, str)
    assert user.password == "password"


@pytest.mark.unit()
def test_user_update_schema() -> None:
    """Test the UserUpdate schema."""
    user = UserUpdate(new_password="new-password", new_password_confirm="new-password")
    assert isinstance(user.new_password, str)
    assert isinstance(user.new_password_confirm, str)
