from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
# from random import randrange

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

app = FastAPI()

myPosts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for post in myPosts:
        if post['id'] == id:
            return post

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": myPosts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(myPosts) + 1 #randrange(0, 100000)
    myPosts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}") #path params are always str
def get_post(id: int):
    post = find_post(id)
    print(post)
    return {"post_detail": post}