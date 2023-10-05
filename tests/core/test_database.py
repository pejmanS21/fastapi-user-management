import pytest
from sqlalchemy.orm import Session

from fastapi_user_management.core.database import get_db


@pytest.mark.unit()
def test_db_session() -> None:
    """Test db session created correctly."""
    # Arrange
    db = next(get_db())

    try:
        # Act
        assert isinstance(db, Session)
        # You can add more assertions based on your specific requirements
    finally:
        # Clean up
        db.close()
