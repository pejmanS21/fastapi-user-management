"""Define examples for openapi documentations."""
from typing import Any

CREATE_USER_OPENAPI_EXAMPLE: dict[str, dict[str, Any]] = {
    "new admin": {
        "summary": "Schema to create new admin",
        "description": "New **admin** creation schema.",
        "value": {
            "fullname": "Rick Sanchez",
            "username": "rick.sanchez@citadel.com",
            "status": "active",
            "roles": [{"name": "admin"}],
            "password": "Wubba-Lubba-Dub-Dub",
        },
    },
    "new user": {
        "summary": "Schema to create new user",
        "description": "New **user** creation schema.",
        "value": {
            "fullname": "Morty Smith",
            "username": "morty.smith@citadel.com",
            "status": "active",
            "roles": [{"name": "user"}],
        },
    },
}
