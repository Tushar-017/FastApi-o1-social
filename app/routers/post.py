from fastapi import Response, status, HTTPException, Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post]) # decorator is actually turn this function into path operation or route
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db:Session=Depends(get_db)):
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # post_dict = post.dict() # convert pydantic model to dictionary
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post  


@router.get("//{id}", response_model=schemas.Post)
def get_post(id: int, db:Session=Depends(get_db)):
    # cursor.execute('''SELECT * from posts WHERE id = %s ''', (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post

@router.delete("//{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session=Depends(get_db)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    found_post = post.first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("//{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db:Session=Depends(get_db)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()



