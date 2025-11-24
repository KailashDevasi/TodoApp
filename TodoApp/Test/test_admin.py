from .utils import *
from ..Routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/admin/get_all")
    assert response.status_code == 200
    assert response.json() == [{"complete" : False, "title" : "Zubdubi du",
        "description" : "zubidubi zubidubi pampara", "id" : 1,
        "priority" : 1, "owner_id" : 1}]


def test_delete_todo(test_todo):
    response = client.delete("/admin/delete/1")
    assert response.status_code == 204
    db = testingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/admin/delete/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}