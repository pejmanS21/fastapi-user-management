"""Create FastAPI App.

Authors: pejmans21
Date: July 6, 2023
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def main() -> dict[str, str]:
    """Simple hello-world.

    Returns:
        dict[str, str]: json to check endpoint works.
    """
    return {"message": "hello-world!", "status": "ok"}
