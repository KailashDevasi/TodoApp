from starlette import status
from TodoApp.Routers.todos import get_db, get_current_user
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user


def test_read_all_authenticated(test_todo):
    response= client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{ "complete" : False, "title" : "Zubdubi du",
        "description" : "zubidubi zubidubi pampara", "id" : 1,
        "priority" : 1, "owner_id" : 1}]



def test_read_one_authenticated(test_todo):
    response= client.get("/todos/get_todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { "complete" : False, "title" : "Zubdubi du",
        "description" : "zubidubi zubidubi pampara",
        "priority" : 1}

def test_read_one_not_authenticated(test_todo):
    response= client.get("/todos/get_todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_body= {
         "title": "New Todo",
        "description": "new todo description",
        "priority": 5, "complete": False
    }
    response = client.post("/todos/add_todo", json= request_body)
    assert response.status_code == status.HTTP_201_CREATED

    db = testingSessionLocal()
    model = db.query(Todos).filter(Todos.title == "New Todo").first()
    assert model is not None
    assert model.title == "New Todo"
    assert model.description == "new todo description"
    assert model.priority == 5
    assert model.complete == False


def test_update_todo(test_todo):
    request_body= {
         "title": "New Todo",
        "description": "new todo description",
        "priority": 5, "complete": False
    }
    response = client.put("/todos/update/1", json= request_body)
    assert response.status_code == status.HTTP_200_OK
    db = testingSessionLocal()
    model = db.query(Todos).filter(Todos.title == "New Todo").first()
    assert model.title == "New Todo"

def test_update_todo_not_found(test_todo):
    request_body= {
         "title": "New Todo",
        "description": "new todo description",
        "priority": 5, "complete": False
        }
    response = client.put("/todos/update/999", json= request_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete(f"/todos/delete/{test_todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = testingSessionLocal()
    model = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/delete/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}