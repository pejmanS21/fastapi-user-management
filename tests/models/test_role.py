import pytest

from fastapi_user_management.models.role import RoleModel, RoleNames


@pytest.mark.unit()
def test_role_database():
    """Test Database object creation correctly."""
    role = RoleModel(name=RoleNames.USER)
    assert isinstance(role.name, RoleNames)
    assert role.name == "user"
