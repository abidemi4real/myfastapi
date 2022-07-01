from typing import Optional
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

from app.database import Base

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False

class User(BaseModel):
    email : EmailStr
    password: str

class GetUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True



class Post(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner : GetUser
    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post : Post
    votes : int
    class Config:
        orm_mode = True

class PostFilter(PostBase):
    id : int
    class Config:
        orm_mode = True




class CreatePost(PostBase):
    pass

class Token(BaseModel):
   
    access_token : str
    token_type : str

class GetToken(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)

