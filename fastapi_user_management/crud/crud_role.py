"""CRUD module for RoleModel table."""
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_user_management.crud.crud_base import CRUDBase
from fastapi_user_management.models.role import RoleModel
from fastapi_user_management.schemas.role import RoleBase, RoleCreate


class CRUDRole(CRUDBase[RoleModel, RoleBase, RoleCreate]):
    """CRUD for roles."""

    def get_by_name(self, db: Session, *, role_obj: RoleBase) -> RoleModel | Any:
        """Get role by name.

        Args:
            db (Session): database session
            role_obj (RoleBase): role object from schema

        Returns:
            RoleModel | Any: loaded object
        """
        return db.execute(
            select(self.model).where(self.model.name == role_obj.name)
        ).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: RoleBase) -> RoleModel:
        """Creat new role in database.

        Args:
            db (Session): database session
            obj_in (RoleBase): role object from schema

        Returns:
            RoleModel: created role
        """
        db_obj: RoleModel = self.model(name=obj_in.name)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


role = CRUDRole(RoleModel)
