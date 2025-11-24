from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Todos(BaseModel):
    title : str = Field(min_length= 3)
    description : str = Field(min_length= 3, max_length= 100)
    priority : int = Field(gt=0, lt=6)
    complete : bool
    model_config =  ConfigDict(from_attributes = True)

class Users(BaseModel):
    username : str = Field(max_length= 15)
    email : str = Field(min_length= 4)
    password : str = Field(min_length=4, max_length=72)
    role : str = Field(default="user")
    phone_number : Optional[str] = Field(default= None)

    model_config = ConfigDict(from_attributes=True)


class ShowUser(BaseModel):
    username : str = Field(max_length= 15)
    email : str = Field(min_length= 4)
    role : str = Field(default="user")
    phone_number : Optional[str] = Field(default= None)

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token : str
    token_type : str