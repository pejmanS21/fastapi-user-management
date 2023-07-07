import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit()
def test_health_check_endpoint(test_app: TestClient) -> None:
    """Test get endpoint in root url.

    Args:
        test_app (TestClient): app instance.
    """
    resp = test_app.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "hello-world!", "status": "ok"}
