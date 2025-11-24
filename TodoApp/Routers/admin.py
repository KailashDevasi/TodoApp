from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from TodoApp import models, schemas
from TodoApp.database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_all")
async def get_all_todos(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    all_post = db.query(models.Todos).all()
    return all_post

@router.delete("/delete/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
