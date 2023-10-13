import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration()
def test_login_for_access_token_success(
    test_app: TestClient, valid_credentials: dict[str, str]
) -> None:
    """Test successful login with valid credentials."""
    response = test_app.post("/auth/token", data=valid_credentials)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


@pytest.mark.integration()
def test_login_for_access_token_invalid_credentials(
    test_app: TestClient, invalid_credentials: dict[str, str]
) -> None:
    """Test login with invalid credentials."""
    response = test_app.post("/auth/token", data=invalid_credentials)
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Incorrect username or password"
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.integration()
def test_login_for_access_token_missing_credentials(
    test_app: TestClient, missing_credentials: dict
) -> None:
    """Test login with missing credentials."""
    response = test_app.post("/auth/token", data=missing_credentials)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
