"""Admin endpoint ``/admin``."""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from fastapi_user_management import crud
from fastapi_user_management.core.database import get_db
from fastapi_user_management.errors.exceptions import PasswordMatchError, UserExistError
from fastapi_user_management.misc import CREATE_USER_OPENAPI_EXAMPLE
from fastapi_user_management.models.user import UserModel
from fastapi_user_management.routes import auth
from fastapi_user_management.schemas.user import BaseUserCreate, UserBase, UserUpdate

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)


@router.get("/user", response_model=list[UserBase])
async def read_users(
    current_user: Annotated[UserModel, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
) -> list[UserModel]:
    """Read all users exist in database.

    Args:
        current_user (Annotated[UserModel, Depends): logged in user.
        db (Session, optional): db session. Defaults to Depends(get_db).
        skip (int, optional): skip. Defaults to 0.
        limit (int, optional): limit. Defaults to 50.

    Raises:
        HTTPException: raise exception for non-admin users with 403 status code.

    Returns:
        list[UserModel]: list of users.
    """
    if crud.user.is_admin(db=db, db_obj=current_user):
        queried_users: list[UserModel] = crud.user.get_multi(
            db=db, skip=skip, limit=limit
        )
        return queried_users
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


@router.post("/user", response_model=UserBase)
async def create_user(
    new_user: Annotated[
        BaseUserCreate, Body(openapi_examples=CREATE_USER_OPENAPI_EXAMPLE)
    ],
    current_user: Annotated[UserModel, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
) -> UserModel:
    """Create new user/admin.

    Args:
        current_user (Annotated[UserModel, Depends): logged in user.
        new_user (BaseUserCreate, optional): new_user fields.
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 403 for non-admin user, access denied.
        HTTPException: 409 if new user data exists in database.

    Returns:
        UserModel: created user.
    """
    if crud.user.is_admin(db=db, db_obj=current_user):
        try:
            created_user: UserModel = crud.user.create(db=db, obj_in=new_user)
            return created_user
        except UserExistError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=e.message
            ) from e
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


@router.delete("/user")
async def delete_user(
    username: EmailStr,
    current_user: Annotated[UserModel, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
) -> Response:
    """Endpoint to delete user.

    Args:
        username (EmailStr): selected user
        current_user (Annotated[UserModel, Depends): logged in user
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 409 Can't remove user with admin role.
        HTTPException: 404 User not found.
        HTTPException: 403 Access denied

    Returns:
        Response: 200 - OK
    """
    if crud.user.is_admin(db=db, db_obj=current_user):
        user: UserModel = crud.user.get_by_username(db=db, username=username)
        if user:
            if not crud.user.is_admin(db=db, db_obj=user):
                crud.user.remove_by_username(db=db, username=username)
                return Response(status_code=status.HTTP_200_OK)
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Can't delete user with admin role!",
                )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


@router.patch("/user")
async def update_user(
    username: EmailStr,
    obj_in: UserUpdate,
    current_user: Annotated[UserModel, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db),
) -> Response:
    """Endpoint to update user.

    Args:
        username (EmailStr): selected user
        obj_in (UserUpdate): update user info
        current_user (Annotated[UserModel, Depends): logged in user
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        HTTPException: 409 Can't remove user with admin role.
        HTTPException: 400 Password doesn't match.
        HTTPException: 403 Access denied

    Returns:
        Response: 200 - OK
    """
    if crud.user.is_admin(db=db, db_obj=current_user):
        user: UserModel = crud.user.get_by_username(username=username)
        if user:
            try:
                crud.user.update(db=db, db_obj=user, obj_in=obj_in)
            except PasswordMatchError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
                ) from e
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
