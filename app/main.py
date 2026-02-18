from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel,Field
from . import models, schema
from .database import SessionLocal, engine
import psycopg
from psycopg import rows
from sqlalchemy.orm import Session
import time
from sqlalchemy import select

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



while True:
    try:
        conn=psycopg.connect(host="localhost", dbname="fastapi", user="postgres",
                            password="please1234", row_factory=rows.dict_row)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

my_post=[{"title":"title of post 1","content":"content of post 1","id":1},
         {"title":"title of post 2","content":"content of post 2","id":2}]

def find_post(id):
    for p in my_post:
        if p['id']==id:
            return p
def find_indexpost(id):
    for i,p in enumerate(my_post):
        if p['id']==id:
            return i

def check_title(t):
    for k in my_post:
        if k['title']==t:
            return k

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/sqlalchemy")
def test_posts():

    return {"status": "success"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    #print(posts)
    stmt=select(models.Post)
    posts=db.execute(stmt).scalars().all()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
    return {"data": new_post}


@app.get("/posts/{id}")
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
    return {"post_detail": result}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@app.put("/posts/{id}")
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


    return {"data":post}