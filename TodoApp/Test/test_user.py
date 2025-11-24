from starlette import status

from .utils import *
from ..Routers.user import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

def test_get_user(test_user):
    response = client.get("/user/get_user")
    assert response.status_code == 200
    assert response.json()["username"] == "KAI"
    assert response.json()["email"] == "myemail@email.com"
    assert response.json()["id"] == 1
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "1234567890"

def test_update_password(test_user):
    request_body = {
        "password": "test_password",
        "new_password": "new_password"
    }
    response = client.put("/user/update_password", json = request_body)
    assert response.status_code == 200
    assert response.json() == {"Message": "Password updated successfully"}

def test_update_password_incorrect_password(test_user):
    request_body = {
        "password": "wrong_password",
        "new_password": "new_password"
    }
    response = client.put("/user/update_password", json= request_body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}


def test_update_pno(test_user):
    response= client.put("/user/update_pno/0987654321")
    assert response.status_code == status.HTTP_200_OK