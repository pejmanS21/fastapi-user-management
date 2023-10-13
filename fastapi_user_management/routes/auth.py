"""Token provider endpoint for JWT."""
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session

from fastapi_user_management import crud
from fastapi_user_management.config import SETTINGS
from fastapi_user_management.core.database import get_db
from fastapi_user_management.models.user import UserModel, UserStatusValues
from fastapi_user_management.schemas.auth import Token, TokenData
from fastapi_user_management.schemas.user import UserBase
from fastapi_user_management.tools.token import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
    },
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> UserModel | Any:
    """Get current user information from token and database.

    Args:
        token (Annotated[str, Depends): access token
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        CREDENTIALS_EXCEPTION: HTTPException with 401 status code.

    Returns:
        UserModel | Any: Current user or Any.
    """
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
        )
        username: EmailStr = payload.get("sub")
        if username is None:  # pragma: no cover
            raise CREDENTIALS_EXCEPTION  # pragma: no cover
        token_data = TokenData(username=username)
    except JWTError as e:  # pragma: no cover
        raise CREDENTIALS_EXCEPTION from e  # pragma: no cover
    user: UserModel | Any = crud.user.get_by_username(
        db=db, username=token_data.username
    )
    if user is None:  # pragma: no cover
        raise CREDENTIALS_EXCEPTION  # pragma: no cover
    return user


async def get_current_active_user(
    current_user: Annotated[UserBase, Depends(get_current_user)]
) -> UserBase:
    """Check if user is active or not.

    Args:
        current_user (Annotated[UserBase, Depends): current user.

    Raises:
        HTTPException: return 400 and not active user.

    Returns:
        UserBase: current user
    """
    if current_user.status is not UserStatusValues.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Endpoint to generate access token for write credentials.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): credentials
        db (Session, optional): db session. Defaults to Depends(get_db).

    Raises:
        HTTPException: raise exception if credentials is incorrect.

    Returns:
        dict[str, str]: access token value & type.s
    """
    user: UserModel | None = crud.user.authenticate(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
