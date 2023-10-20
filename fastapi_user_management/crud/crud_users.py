"""CRUD module for UserModel table."""
import secrets
from datetime import datetime
from typing import Any

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_user_management import crud
from fastapi_user_management.crud.crud_base import CRUDBase
from fastapi_user_management.errors.exceptions import PasswordMatchError, UserExistError
from fastapi_user_management.models.role import RoleModel, RoleNames
from fastapi_user_management.models.user import UserModel, UserStatusValues
from fastapi_user_management.schemas.user import BaseUserCreate, UserCreate, UserUpdate
from fastapi_user_management.tools.encryption import get_password_hash, verify_password

PASSWORD_LENGTH = 8


class CRUDUser(CRUDBase[UserModel, BaseUserCreate | UserCreate, UserUpdate]):
    """CRUD for user database model."""

    def get_by_username(self, db: Session, *, username: EmailStr) -> UserModel | None:
        """Get user by username.

        Args:
            db (Session): database session
            username (EmailStr): username

        Returns:
            UserModel | None: selected user
        """
        return db.execute(
            select(self.model).where(self.model.username == username)
        ).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: BaseUserCreate) -> UserModel:
        """Create new user.

        Args:
            db (Session): database session
            obj_in (BaseUserCreate): user data based on schema

        Returns:
            UserModel: created user
        """
        if self.get_by_username(db=db, username=obj_in.username):
            raise UserExistError
        roles: list[RoleModel] = []
        for role_obj in obj_in.roles:
            role = (
                crud.role.get_by_name(db=db, role_obj=role_obj)
                if crud.role.get_by_name(db=db, role_obj=role_obj) is not None
                else crud.role.create(db=db, obj_in=role_obj)
            )
            roles.append(role)

        db_obj: UserModel = self.model(
            username=obj_in.username,
            fullname=obj_in.fullname,
            password=get_password_hash(
                obj_in.password
                if obj_in.password is not None
                else secrets.token_urlsafe(PASSWORD_LENGTH)
            ),
            created_at=datetime.utcnow(),
            status=(
                obj_in.status if obj_in.status is not None else UserStatusValues.PENDING
            ),
            roles=roles,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: UserModel,
        obj_in: UserUpdate | dict[str, Any],
    ) -> UserModel:
        """Update user info.

        Args:
            db (Session): database session
            db_obj (UserModel): selected user
            obj_in (UserUpdate | dict[str, Any]): updating data

        Raises:
            PasswordMatchError: raise if password and its confirmation doesn't match

        Returns:
            UserModel: selected user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["new_password"] == update_data["new_password_confirm"]:
            hashed_password = get_password_hash(update_data["new_password"])
            del update_data["new_password"]
            update_data["password"] = hashed_password
        else:
            raise PasswordMatchError
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, username: EmailStr, password: str
    ) -> UserModel | None:
        """Check user credentials for authentication.

        Args:
            db (Session): database session
            username (EmailStr): user cred
            password (str): user cred

        Returns:
            UserModel | None: logged in user or None
        """
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def remove_by_username(self, db: Session, *, username: EmailStr) -> UserModel:
        """Delete user by username.

        Args:
            db (Session): database session
            username (EmailStr): username

        Returns:
            UserModel: deleted user
        """
        selected_user = self.get_by_username(db=db, username=username)
        return super().remove(db, id=selected_user.id)

    def is_active(self, user: UserModel) -> bool:
        """Check user status.

        Args:
            user (UserModel): selected user

        Returns:
            bool: True if status is `active`
        """
        return user.status is UserStatusValues.ACTIVE

    def is_admin(self, db: Session, db_obj: UserModel) -> bool:
        """Check for admin role in user.

        Args:
            db (Session): database session
            db_obj (UserModel): selected user

        Returns:
            bool: True if user is admin.
        """
        admin_role = db.execute(
            select(RoleModel).where(RoleModel.name == RoleNames.ADMIN)
        ).scalar_one_or_none()
        return admin_role in db_obj.roles


user = CRUDUser(UserModel)
