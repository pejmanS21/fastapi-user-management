import pytest

from fastapi_user_management.models.role import RoleNames
from fastapi_user_management.schemas.role import RoleBase


@pytest.mark.unit()
def test_role_base_schema():
    """Test RoleBase Schema."""
    role1 = RoleBase()
    role2 = RoleBase(name=RoleNames.USER)

    assert isinstance(role1, RoleBase)
    assert role1.name is None
    assert isinstance(role2, RoleBase)
    assert isinstance(role2.name, RoleNames)
