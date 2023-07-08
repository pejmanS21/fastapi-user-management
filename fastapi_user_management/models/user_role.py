"""Relationship Table for User and Role Tables."""

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_user_management.models.base import Base


class UserRoleModel(Base):
    """UserRole Table mapping user_id to role_id."""

    __tablename__ = "user_role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_account.id"))
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"))
