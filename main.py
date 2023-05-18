from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
# from random import randrange

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

app = FastAPI()

myPosts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

#not the best way to retrieve data
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(myPosts) + 1 #randrange(0, 100000)
    myPosts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}") #path params are always str
def get_post(id: int, res: Response): #res not needed
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}

# Keep aware of your routes as similar path may hit because of ordering
# @app.get("/posts/latest")
# def get_latest_post():
#     post = myPosts[len(myPosts)-1]
#     return {"latest post": post}