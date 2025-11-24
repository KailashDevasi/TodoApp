from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from TodoApp import models, schemas
from TodoApp.database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(prefix="/user", tags=["User"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=4)



@router.get("/get_user")
async def get_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_details = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    return user_details

@router.put("/update_password")
async def update_password(request: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if not pwd_context.verify(request.password, user_model.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    user_model.password = pwd_context.hash(request.new_password)
    db.commit()
    db.refresh(user_model)
    return {"Message": "Password updated successfully"}

@router.put("/update_pno/{ph_number}")
async def update_pno(ph_number: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_model= db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    user_model.phone_number = ph_number
    db.commit()
    db.refresh(user_model)
    return {"Message": "Phone number updated successfully"}