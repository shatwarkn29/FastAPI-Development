from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
    title:str
    content:str
    published: bool = True

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass 

class PostUpdate(PostBase):
    pass

class User_out(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True

class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : User_out
    
    class config:
        orm_mode = True

class Post_out(BaseModel):
    post : PostResponse
    votes : int

class User_Create(BaseModel):
    email: EmailStr
    password : str



class Get_User(User_out):
    pass    


class Userlogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : int


class Vote(BaseModel):
    post_id : int
    dir : conint(ge=0 ,le=1)