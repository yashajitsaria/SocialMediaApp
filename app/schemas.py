from datetime import datetime
from pydantic import BaseModel

#Post schema
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