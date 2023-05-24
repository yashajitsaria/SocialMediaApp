from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routes import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)

#Hello World
@app.get("/")
def root():
    return {"message": "Hello World"}
