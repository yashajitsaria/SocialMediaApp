from datetime import datetime
from pydantic import BaseModel, EmailStr

#Post Schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at = datetime.now()

    class Config:
        orm_mode = True

#User Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at = datetime.now()

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str