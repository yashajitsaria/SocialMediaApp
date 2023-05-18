from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}

@app.post("/posts")
def create_posts(post: Post):
    print(post.dict())
    return {"data": f"title: {post.title}, content: {post.content}"}