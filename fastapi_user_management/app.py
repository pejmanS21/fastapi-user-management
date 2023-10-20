"""Create FastAPI App.

Authors: pejmans21
Date: July 6, 2023
"""

from fastapi import FastAPI
from sqlalchemy.orm import Session

from fastapi_user_management.config import SETTINGS
from fastapi_user_management.core.database import engine
from fastapi_user_management.core.init_db import init_db
from fastapi_user_management.models.base import Base
from fastapi_user_management.routes import admin, auth


def create_db_and_tables() -> None:
    """Create db and tables."""
    Base.metadata.create_all(engine)


app = FastAPI(
    title=SETTINGS.TITLE,
    description=SETTINGS.DESCRIPTION,
    docs_url=SETTINGS.DOCS_URL,
    redoc_url=SETTINGS.REDOC_URL,
)


@app.on_event("startup")
def on_startup() -> None:
    """Initiate database on startup."""
    create_db_and_tables()
    with Session(bind=engine) as session:
        init_db(db=session)


@app.get("/")
def main() -> dict[str, str]:
    """Simple hello-world.

    Returns:
        dict[str, str]: json to check endpoint works.
    """
    return {"message": "hello-world!", "status": "ok"}


app.include_router(admin.router)
app.include_router(auth.router)
