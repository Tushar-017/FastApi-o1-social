from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


load_dotenv()


app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

@app.get("/") # decorator to define a GET endpoint
async def root():
    return {"message": "Hello, World!"}

