"""Module to define Role schemas."""
from pydantic import BaseModel

from fastapi_user_management.models.role import RoleNames


class RoleBase(BaseModel):
    """Base Schema for role."""

    name: RoleNames | None = None
