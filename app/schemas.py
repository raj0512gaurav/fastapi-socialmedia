from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

'''
Pydantic Models
- Schema/Pydantic Models define the structure of a request and response
- This ensure that when a user wants to create a post, the request will
only go through if it has a "title" and "content" in the body
'''
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserOutPost(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    location: Optional[str]=None
    published: bool=True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: Optional[str]=None
    content: Optional[str]=None

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOutPost

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]=None

class DirectionEnum(int, Enum):
    zero = 0
    one = 1

class Vote(BaseModel):
    post_id: int
    dir: DirectionEnum