"""Define Role Model Table."""
from enum import StrEnum, auto

from sqlalchemy import Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_user_management.models.base import Base


class RoleNames(StrEnum):
    """Enum Values for Roles.

    Values:
        ADMIN: admin
        USER: user
    """

    ADMIN = auto()
    USER = auto()


class RoleModel(Base):
    """Role Database Table."""

    __tablename__ = "role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[RoleNames] = mapped_column(
        Enum(RoleNames), nullable=False, unique=True
    )

    def __repr__(self) -> str:
        """Database object representation.

        Returns:
            str: object
        """
        return f"<Role(name={self.name})>"
