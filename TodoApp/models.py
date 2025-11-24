from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Todos(Base):
    __tablename__ = 'todos'
    id = Column (Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column (Integer)
    complete = Column (Boolean, default=False)
    owner_id = Column (Integer, ForeignKey("users.id"))


class Users(Base):
    __tablename__ = 'users'
    id = Column (Integer, primary_key=True, index=True)
    username = Column (String)
    email = Column (String)
    password = Column (String)
    role = Column(String)
    phone_number = Column (String)