from typing import Any

import pytest
from fastapi.testclient import TestClient

from fastapi_user_management.schemas.user import UserBase


@pytest.fixture(scope="module")
def get_authorization_headers(
    test_app: TestClient, valid_credentials: dict[str, str]
) -> dict[str, str]:
    """Get access token for auth_required endpoints."""
    auth_response = test_app.post("/auth/token", data=valid_credentials)
    headers: dict[str, str] = {
        "Authorization": f'Bearer {auth_response.json()["access_token"]}'
    }
    return headers


@pytest.mark.integration()
def test_read_users_as_admin(
    test_app: TestClient, get_authorization_headers: dict[str, str]
) -> None:
    """Test reading users as an admin."""
    response = test_app.get("/admin/user", headers=get_authorization_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for user_data in data:
        user = UserBase(**user_data)
        assert user.username is not None
        assert user.status is not None


@pytest.mark.integration()
def test_create_user_as_admin(
    test_app: TestClient,
    new_user_data: dict[str, str],
    get_authorization_headers: dict[str, str],
) -> None:
    """Test creating a new user as an admin."""
    response = test_app.post(
        "/admin/user", json=new_user_data, headers=get_authorization_headers
    )
    assert response.status_code == 200
    created_user = UserBase(**response.json())
    assert created_user.username == new_user_data["username"]


@pytest.mark.integration()
def test_create_user_existing_data_as_admin(
    test_app: TestClient,
    existing_user_data: dict[str, str],
    get_authorization_headers: dict[str, str],
) -> None:
    """Test creating a user with existing data as an admin."""
    test_app.post(
        "/admin/user", json=existing_user_data, headers=get_authorization_headers
    )  # Create the user first
    response = test_app.post(
        "/admin/user", json=existing_user_data, headers=get_authorization_headers
    )  # Try to create the same user again
    assert response.status_code == 409  # Conflict
    data = response.json()
    assert "detail" in data
    assert "Username already exist!" == data["detail"]


@pytest.mark.integration()
def test_read_users_as_non_admin(
    test_app: TestClient, new_user_data: dict[str, Any]
) -> None:
    """Test reading users as a non-admin."""
    auth_response = test_app.post(
        "/auth/token",
        data={
            "username": new_user_data["username"],
            "password": new_user_data["password"],
        },
    )
    headers: dict[str, str] = {
        "Authorization": f'Bearer {auth_response.json()["access_token"]}'
    }
    response = test_app.get("/admin/user", headers=headers)
    assert response.status_code == 403  # Access denied for non-admin


@pytest.mark.integration()
def test_read_users_as_deactive_users(
    test_app: TestClient, existing_user_data: dict[str, Any]
) -> None:
    """Test reading users as a non-admin."""
    auth_response = test_app.post(
        "/auth/token",
        data={
            "username": existing_user_data["username"],
            "password": existing_user_data["password"],
        },
    )
    headers: dict[str, str] = {
        "Authorization": f'Bearer {auth_response.json()["access_token"]}'
    }
    response = test_app.get("/admin/user", headers=headers)
    assert response.status_code == 400  # Inactive user
    assert response.json()["detail"] == "Inactive user"


@pytest.mark.integration()
def test_create_user_as_non_admin(
    test_app: TestClient, new_user_data: dict[str, Any]
) -> None:
    """Test creating a new user as a non-admin."""
    auth_response = test_app.post(
        "/auth/token",
        data={
            "username": new_user_data["username"],
            "password": new_user_data["password"],
        },
    )
    headers: dict[str, str] = {
        "Authorization": f'Bearer {auth_response.json()["access_token"]}'
    }
    response = test_app.post("/admin/user", json=new_user_data, headers=headers)
    assert response.status_code == 403  # Access denied for non-admin
