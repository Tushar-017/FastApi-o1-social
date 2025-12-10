from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


load_dotenv()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastApi', user='postgres', password=os.getenv('DB_PASSWORD'), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Databses connection was succesfull!')
        break
    except Exception as error:
        print('Connection to databse failed')
        print('Error: ', error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

@app.get("/") # decorator to define a GET endpoint
async def root():
    return {"message": "Hello, World!"}

