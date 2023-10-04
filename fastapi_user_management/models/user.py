"""Module to create User Database Model in SQLAlchemy."""

from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import (
    Mapped,
    backref,
    mapped_column,
    relationship,
    validates,
)

from fastapi_user_management.models.base import Base
from fastapi_user_management.models.role import RoleModel
from fastapi_user_management.models.user_role import UserRoleModel  # noqa: F401


class UserStatusValues(StrEnum):
    """User Status Enum.

    Values:
        ACTIVE: active
        PENDING: pending
        DEACTIVATE: deactivate
    """

    ACTIVE = auto()
    PENDING = auto()
    DEACTIVATE = auto()


class UserModel(Base):
    """User Database Model known as user_account.

    Raises:
        ValueError: raise if email doesn't contain `@`.
    """

    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False, unique=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, unique=False
    )
    status: Mapped[UserStatusValues] = mapped_column(
        Enum(UserStatusValues), nullable=False, default=UserStatusValues.PENDING
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        "RoleModel", secondary="user_role", backref=backref("users", lazy="dynamic")
    )

    @validates("username")
    def validate_email(self, key: str, username: str) -> str:
        """Simple email validator.

        Args:
            key (str): Database key
            username (str): value of email

        Raises:
            ValueError: Failed simple email validation
        """
        if "@" not in username:
            raise ValueError("Failed simple email validation")
        return username

    def __repr__(self) -> str:
        """Database object representation.

        Returns:
            str: object
        """
        return (
            f"<User(username={self.username}, fullname={self.fullname},"
            f" status={self.status})>"
        )
