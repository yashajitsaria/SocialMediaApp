from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

#Post schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

app = FastAPI()

#temporary replacement for a db
myPosts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

#Find a post
def find_post(id):
    for post in myPosts:
        if post['id'] == id:
            return post

#Find index of a post      
def find_index_post(id):
    for index, post in enumerate(myPosts):
        if post['id'] == id:
            return index

#Hello World
@app.get("/")
def root():
    return {"message": "Hello World"}

#Get all Posts
@app.get("/posts")
def get_posts():
    return {"data": myPosts}

#Create a Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    myPosts.append(post_dict)
    return {"data": post_dict}

#Get a specific Post
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

#Delete a Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    myPosts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update a Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict["id"] = id
    myPosts[index] = post_dict
    return {"data": post_dict}