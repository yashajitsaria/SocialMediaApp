from fastapi import Body, FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/posts")
def create_posts(post: Post):
    return {"data": f"title: {post.title}, content: {post.content}"}