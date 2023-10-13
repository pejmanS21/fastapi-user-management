"""Define schame for auth."""
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token Response schema for token generator endpoint.

    Args:
        access_token
        token_type
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""

    username: EmailStr | None = None
