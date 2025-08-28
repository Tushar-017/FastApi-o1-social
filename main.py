from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # published: bool = True


@app.get("/") # decorator to define a GET endpoint
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts") # decorator to define a GET endpoint
async def root():
    return {"data": "This is your posts!"}


@app.post("/createpost")
def create_post(post: Post = Body(...)):
    print(post)
    return {"new_post": f"title: {post.title} content: {post.content}"}