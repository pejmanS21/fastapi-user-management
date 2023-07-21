import pytest

from fastapi_user_management.errors.exceptions import PasswordMatchError


@pytest.mark.unit()
def test_password_error_default_message() -> None:
    """Test PasswordMatchError default massage."""
    error = PasswordMatchError()
    assert str(error) == "Password doesn't match!"


@pytest.mark.unit()
def test_password_error_custom_message() -> None:
    """Test PasswordMatchError custom message."""
    error_msg: str = "Error Message!"
    error = PasswordMatchError(message=error_msg)
    assert str(error) == error_msg
