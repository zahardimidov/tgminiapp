from fastapi.testclient import TestClient
from logging import Logger

def test_root(client: TestClient):
    response = client.get("/ping")

    assert response.status_code == 200


