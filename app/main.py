from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

#Post schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

#not the best way
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='elephant', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as err:
        print("Connecting to Database failed")
        print("Error: ", err)
        time.sleep(2)

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
def get_all_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

#Create a Post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    return {"data": newPost}

#Get a Post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}

#Delete a Post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update a Post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    conn.commit()
    return {"updated data": post}