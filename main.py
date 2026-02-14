from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel,Field
from random import randrange
import psycopg
from psycopg import rows
import time

app = FastAPI()

class Post(BaseModel):
    title:str = Field(min_length=5, max_length=50)
    content:str = Field(min_length=10)
    published: bool = True
    rating: Optional[int] = Field(ge=1, le=5, description="rating must bbe between 1 and 5")
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

@app.get("/posts")
def get_posts():
    return {"data":my_post}

@app.post("/posts")
#if the same title already exist, then we need to return 400 error
#api verifies the schema
def create_posts(post: Post, response: Response):
    #converting pydantic instance into dict and storing it
    post_dict = post.dict()
    #creating a random id
    post_dict['id'] = randrange(0,1000000)
    dup_title=check_title(post_dict['title'])
    if dup_title:
        response.status_code= status.HTTP_404_NOT_FOUND
        return "error"
    #appending it to the main db
    else:
        my_post.append(post_dict)
        #returning it to user
        return {"data":post_dict}

@app.get("/posts/{id}")
# ineed to modify my post so that
def get_post(id:int, response: Response):
    post= find_post(id)
    if not post:
        response.status_code= status.HTTP_404_NOT_FOUND
        return {"message":f"post with id {id} was not found"}
    return {"post_detail":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    post= find_indexpost(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with this id does not exits")
    my_post.pop(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index= find_indexpost(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    post_dict= post.dict()
    post_dict['id']=id
    my_post[index]=post_dict
    return {"data":post_dict}