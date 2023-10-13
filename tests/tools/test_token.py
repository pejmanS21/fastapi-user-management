from datetime import timedelta

import pytest
from jose import jwt

from fastapi_user_management.config import SETTINGS
from fastapi_user_management.tools.token import create_access_token


@pytest.mark.unit()
def test_create_access_token_with_expiration() -> None:
    """Test access_token function specified timedelta."""
    data = {"sub": "user_id"}
    expires_delta = timedelta(minutes=30)

    token = create_access_token(data, expires_delta)

    decoded = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM])
    assert decoded["sub"] == "user_id"
    assert "exp" in decoded
    assert isinstance(decoded["exp"], int)


@pytest.mark.unit()
def test_create_access_token_without_expiration() -> None:
    """Test access_token with default timedelta."""
    data = {"sub": "user_id"}

    token = create_access_token(data)

    decoded = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM])
    assert decoded["sub"] == "user_id"
    assert "exp" in decoded
    assert isinstance(decoded["exp"], int)
