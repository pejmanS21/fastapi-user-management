"""Token generation function."""
from datetime import datetime, timedelta

from jose import jwt

from fastapi_user_management.config import SETTINGS


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate access token for specified time, default set to 15 minutes.

    Args:
        data (dict): Information related to user.
        expires_delta (timedelta | None, optional): Token expiration time. Defaults to None.

    Returns:
        str: access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.SECRET_KEY, algorithm=SETTINGS.ALGORITHM
    )
    return encoded_jwt
