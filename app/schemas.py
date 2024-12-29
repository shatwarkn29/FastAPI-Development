from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
    title:str
    content:str
    published: bool = True

class PostBase(BaseModel):
    """Configuration for PostBase class."""
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    """Schema for creating a new post."""
    pass

class PostUpdate(PostBase):
    """Schema for updating a post."""
    pass

class Userout(BaseModel):
    """Schema for user output, including user details."""
    id : int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    """Schema for responding with a post (including metadata)."""
    id : int
    created_at : datetime
    owner_id : int
    owner : Userout
    class Config:
        from_attributes = True

class Postout(BaseModel):
    """Schema for post with response data and vote count."""
    post : PostResponse
    votes : int

class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr
    password : str

class GetUser(Userout):
    """Schema for retrieving user information."""
    pass

class Userlogin(BaseModel):
    """Schema for user login with email and password."""
    email : EmailStr
    password : str

class Token(BaseModel):
    """Schema for returning a token."""
    access_token : str
    token_type : str


class TokenData(BaseModel):
    """Schema for the data embedded in the token."""
    id : int


class Vote(BaseModel):
    """Schema for vote information related to a post."""
    post_id : int
    dir : conint(ge=0 ,le=1)
