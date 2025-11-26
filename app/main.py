from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import time
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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


@app.get("/") # decorator to define a GET endpoint
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts") # decorator is actually turn this function into path operation or route
async def get_posts():
    cursor.execute("""SELECT * from posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    # post_dict = post.dict() # convert pydantic model to dictionary
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    return {"data": new_post}  


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute('''SELECT * from posts WHERE id = %s ''', (str(id)))
    post = cursor.fetchone()
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ''', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"data": updated_post}