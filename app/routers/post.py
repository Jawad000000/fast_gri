from .. import models, schema
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import select
from typing import  List

router = APIRouter()



@router.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    #print(posts)
    stmt=select(models.Post)
    posts=db.execute(stmt).scalars().all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
#prevent duplicate titles
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    #run a select query to chcek if title exists.if exists raise http
    
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)
    #                RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # return {"data":new_post}
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/posts/{id}", response_model=schema.Post)
# ineed to modify my post so that
def get_post(id:int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts where id=%s""",(id,))
    # np=cursor.fetchone()
    # if not np:
    #     response.status_code= status.HTTP_404_NOT_FOUND
    #     return {"message":f"post with id {id} was not found"}
    # return {"post_detail":np}
    stmt=select(models.Post).where(models.Post.id==id)
    result=db.execute(stmt).scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return result

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s returning *""",(id,))
    # delete_post=cursor.fetchone()
    # conn.commit()

    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with this id does not exits")
    

    db.delete(post)
    db.commit() 

    return {"message": "Post deleted successfully"}

@router.put("/posts/{id}", response_model=schema.Post)
def update_post(id:int, updated_post:schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s
    #                WHERE id=%s returning * """,(post.title, post.content, post.published, id,))
    # index=cursor.fetchone()
    # conn.commit()
    post = db.get(models.Post, id)


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
    post.title = updated_post.title
    post.content = updated_post.content

    db.commit()
    db.refresh(post)

    return post
