from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel,Field
from . import models
from .database import engine, get_db
import psycopg
from psycopg import rows
from sqlalchemy.orm import Session
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title:str = Field(min_length=5, max_length=50)
    content:str = Field(min_length=10)
    published: bool = True

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
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    print(posts)
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
#prevent duplicate titles
def create_posts(post: Post, ):
    #run a select query to chcek if title exists.if exists raise http
    
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)
                   RETURNING * """,
                   (post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}
@app.get("/posts/{id}")
# ineed to modify my post so that
def get_post(id:int, response: Response):
    cursor.execute("""SELECT * FROM posts where id=%s""",(id,))
    np=cursor.fetchone()
    if not np:
        response.status_code= status.HTTP_404_NOT_FOUND
        return {"message":f"post with id {id} was not found"}
    return {"post_detail":np}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s returning *""",(id,))
    delete_post=cursor.fetchone()
    conn.commit()


    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with this id does not exits")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s
                   WHERE id=%s returning * """,(post.title, post.content, post.published, id,))
    index=cursor.fetchone()
    conn.commit()
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    return {"data":index}