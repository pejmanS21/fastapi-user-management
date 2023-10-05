"""Initiate Database and create admin user."""
from typing import Any

from sqlalchemy.orm import Session

from fastapi_user_management import crud
from fastapi_user_management.config import SETTINGS
from fastapi_user_management.models.role import RoleNames
from fastapi_user_management.models.user import UserModel, UserStatusValues
from fastapi_user_management.schemas.role import RoleBase
from fastapi_user_management.schemas.user import UserCreate


def init_db(db: Session) -> None:
    """Initiate database, create admin user if not exists.

    Args:
        db (Session): database session.
    """
    user: UserModel | Any = crud.user.get_by_username(db, username=SETTINGS.ADMIN_EMAIL)
    if not user:
        user_in = UserCreate(
            username=SETTINGS.ADMIN_EMAIL,
            fullname=SETTINGS.ADMIN_FULLNAME,
            password=SETTINGS.ADMIN_PASSWORD,
            status=UserStatusValues.ACTIVE,
            roles=[RoleBase(name=RoleNames.ADMIN)],
        )
        crud.user.create(db, obj_in=user_in)
