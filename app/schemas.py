

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


#used to convert alchamy model to pydantic model so chat it can be further converted into dicts 


#pydantic model used to add validation to the data entered by the user like in create and update requests 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase):
    id: int
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str




class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)