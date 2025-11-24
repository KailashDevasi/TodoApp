from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from TodoApp.database import Base
from fastapi.testclient import TestClient
from TodoApp.main import app
from ..models import Todos, Users
from ..Routers.auth import pwd_context
import pytest

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine (SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass= StaticPool)

testingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base.metadata.create_all(bind= engine)

def override_get_db():
    db = testingSessionLocal()
    try:
        yield db
    finally: db.close()

def override_get_current_user():
    return {"username": "KAI", "id": 1, "role": "admin"}

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        id = 1,
        title = "Zubdubi du",
        description = "zubidubi zubidubi pampara",
        priority = 1,
        complete = False,
        owner_id = 1
    )
    db = testingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        id = 1,
        username = "KAI",
        email = "myemail@email.com",
        password = pwd_context.hash("test_password"),
        role = "admin",
        phone_number = "1234567890"
    )
    db = testingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


