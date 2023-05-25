from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#Get all Posts
@router.get("/", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db), userID: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

#Create a Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), userID: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()

    print(userID)

    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

#Get a Post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), userID: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

#Delete a Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), userID: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update a Post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), userID: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return post_query.first()
