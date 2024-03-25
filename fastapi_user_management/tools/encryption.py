"""Encrypt password."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check password with hashed password.

    Args:
        plain_password (str): plain text password
        hashed_password (bool): encrypted password

    Returns:
        bool: password match or not?
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get plain password and hash woth bcrypt.

    Args:
        password (str): plain password

    Returns:
        str: hashed password
    """
    return pwd_context.hash(password)
