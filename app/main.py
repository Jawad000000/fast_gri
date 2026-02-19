from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel,Field
from . import models, schema, utils
from .database import engine
import psycopg
from psycopg import rows
from sqlalchemy.orm import Session
import time
from sqlalchemy import select
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

app.include_router(post.router)
app.include_router(user.router)



@app.get("/")
def root():
    return {"message":"Hello World"}
