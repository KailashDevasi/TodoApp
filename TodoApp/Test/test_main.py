from fastapi.testclient import TestClient
from TodoApp.main import app
from fastapi import status

client = TestClient(app)

def test_return_health():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Status": "Healthy"}