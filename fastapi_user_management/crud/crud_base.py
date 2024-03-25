"""Base CRUD module for inheritance."""

from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_user_management.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD moduel."""

    def __init__(self, model: type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | Any:
        """Get object by id.

        Args:
            db (Session): database session
            id (Any): row id

        Returns:
            ModelType | Any: _description_
        """
        return db.execute(
            select(self.model).where(self.model.id == id)
        ).scalar_one()  # pragma: no cover

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 50
    ) -> list[ModelType] | Any:
        """Get list of object.

        Args:
            db (Session): database session
            skip (int, optional): skip an id. Defaults to 0.
            limit (int, optional): loading limit. Defaults to 50.

        Returns:
            list[ModelType] | Any: list of objects
        """
        return (
            db.execute(select(self.model).offset(skip).limit(limit)).scalars().all()
        )  # pragma: no cover

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create new object.

        Args:
            db (Session): database session
            obj_in (CreateSchemaType): new object based on schema

        Returns:
            ModelType: created object
        """
        obj_in_data = jsonable_encoder(obj_in)  # pragma: no cover
        db_obj = self.model(**obj_in_data)  # pragma: no cover
        db.add(db_obj)  # pragma: no cover
        db.commit()  # pragma: no cover
        db.refresh(db_obj)  # pragma: no cover
        return db_obj  # pragma: no cover

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Update existing record.

        Args:
            db (Session): database session
            db_obj (ModelType): existing record
            obj_in (UpdateSchemaType | dict[str, Any]): updated information

        Returns:
            ModelType: updated record
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):  # pragma: no cover
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)  # pragma: no cover
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove existing object.

        Args:
            db (Session): database session
            id (int): object id

        Returns:
            ModelType: deleted object
        """
        obj: ModelType = db.execute(
            select(self.model).where(self.model.id == id)
        ).scalar_one()
        db.delete(obj)  # type: ignore  # `[no-untyped-call]`
        db.commit()
        return obj
