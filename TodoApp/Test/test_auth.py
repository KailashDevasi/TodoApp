from fastapi import HTTPException
from .utils import *
from ..Routers.auth import get_db, authenticate_user, create_access_token, get_current_user, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = testingSessionLocal()
    user = authenticate_user(test_user.username, "test_password", db)
    assert user is not None
    wrong_user = authenticate_user("wrong_username", "test_password", db)
    assert wrong_user is False


def test_create_access_token(test_user):
    username = "test_user"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == username
    assert payload["id"] == user_id
    assert payload["role"] == role


@pytest.mark.asyncio
async def test_get_current_user(test_user):
    encode= {"sub": test_user.username, "id": test_user.id, "role": test_user.role}
    token = jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

    user = await get_current_user(token)
    assert user == {"username": test_user.username, "id": test_user.id, "role": test_user.role}

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    encode = {"sub": "invalid_user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"










def test_get_all_users(test_user):
    response = client.get("/auth/")
    assert response.status_code == 200
    assert response.json() == [{
        "username": "KAI",
        "email": "myemail@email.com",
        "role": "admin",
        "phone_number": "1234567890"
    }]