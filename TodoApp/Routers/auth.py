import datetime
from datetime import timedelta, timezone, datetime
from fastapi import APIRouter
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from typing import List
from sqlalchemy.orm import Session
from starlette import status
from TodoApp import models, schemas
from TodoApp.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2bearer = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


#elements for token
SECRET_KEY = 'hYLkWYiuE0sppw3cICek6gMkepbscs143BMTP7jTcmc='
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

template = Jinja2Templates(directory= "TodoApp/templates")

### Pages ###


@router.get("/login-page")
def render_login_page(request: Request):
    return template.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return template.TemplateResponse("register.html", {"request": request})


### Endpoints ###

#-------------------------- Authentication ----------------------------
#           just verifying if the credentials match, SIMPLE
def authenticate_user(username, password, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

#--------------------------------- Encoding T_T ------------------------------------------------
#                           encoding and creating token
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta = None):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


#--------------------------------- Decoding T_T ------------------------------------------------
#                     decoding and returning current user details
async def get_current_user(token: str = Depends(oauth2bearer), request: Request = None):
    # 1) If token not found in Authorization header → try cookie
    if not token and request:
        token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload.get("sub"),
            "id": payload.get("id"),
            "role": payload.get("role")
        }
    except Exception:
        return None

async def get_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            return None
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        return None




#-------------------------------token endpoint------------------------------------------------

@router.post("/token", response_model=schemas.Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(request.username, request.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, user.role, expires_delta=timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


#--------------------User endpoints---------------------

@router.get("/", response_model=List[schemas.ShowUser])
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users


@router.get("/{user_id}", response_model=schemas.ShowUser)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(request : schemas.Users, db: Session = Depends(get_db)):
    new_user = models.Users(username= request.username, email= request.email, password= pwd_context.hash(request.password), role= request.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}/", response_model=schemas.ShowUser)
async def update_user(user_id: int, request: schemas.Users, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = request.username
    user.email = request.email
    user.password = pwd_context.hash(request.password)
    user.role = request.role
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
