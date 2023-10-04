"""Create FastAPI App.

Authors: pejmans21
Date: July 6, 2023
"""

from fastapi import FastAPI

from fastapi_user_management.config import SETTINGS

app = FastAPI(
    title=SETTINGS.TITLE,
    description=SETTINGS.DESCRIPTION,
    docs_url=SETTINGS.DOCS_URL,
    redoc_url=SETTINGS.REDOC_URL,
)


@app.get("/")
def main() -> dict[str, str]:
    """Simple hello-world.

    Returns:
        dict[str, str]: json to check endpoint works.
    """
    return {"message": "hello-world!", "status": "ok"}
