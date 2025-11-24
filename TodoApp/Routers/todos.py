from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette import status
from TodoApp import models, schemas
from TodoApp.database import SessionLocal
from .auth import get_current_user, get_user_from_cookie
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..models import Todos

templates = Jinja2Templates(directory= "TodoApp/templates")


router = APIRouter(prefix= "/todos", tags=["Todos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_user_from_cookie(request)
        if user is None:
            return redirect_to_login()
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todos.html", {"request": request, "todos": todos, "user": user})
    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_add_todo_page(request: Request, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = await get_user_from_cookie(request)
    if user is None:
        return redirect_to_login()
    return templates.TemplateResponse("add-todos.html", {"request": request, "user": user})

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_user_from_cookie(request)
    if user is None:
        return redirect_to_login()
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

### Endpoints ###
@router.get("/")
async def get_all_todos(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    all_post = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()
    return all_post

@router.get("/get_todo/{post_id}", response_model=schemas.Todos)
async def get_todo(post_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == post_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/add_todo", status_code=status.HTTP_201_CREATED, response_model=schemas.Todos)
async def create_todo(request: schemas.Todos , user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_post = models.Todos(**request.model_dump(), owner_id=user.get("id"))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/update/{post_id}", response_model=schemas.Todos)
async def update_todo(request: schemas.Todos, post_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo = db.query(models.Todos).filter(models.Todos.id == post_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = request.title
    todo.description = request.description
    todo.priority = request.priority
    todo.complete = request.complete
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/delete/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
