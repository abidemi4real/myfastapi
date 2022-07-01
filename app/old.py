#from curses.ascii import HT
#from tkinter import Y
import enum
from os import stat
import time
from typing import Optional
from click import command
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models

from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title : str
    content : str
    published : bool = False


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='ridrid22', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print ("Database connected succssfully")
        break
    except Exception as error:
        print ("Unable to connect to db")
        print ("Error due to " , error)
        time.sleep(5)

# function for finding post
my_post = [{"title": "First title","content": "First COntent", "id": 1},{"title": "Second title","content": "Second COntent", "id": 2},{"title": "didt title","content": "Third COntent", "id": 5}]
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
# function for finding index of a post to delete
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message" : "All i"}



@app.get("/sqlalchmey")
def testing (db: Session = Depends(get_db) ):
    return {"status" : "Success"}

#get all post
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    #print (posts)
    return {"message" : posts}
    #return {"Data" : my_post}

# create a new post

@app.post("/posts")
def posts(post : Post):
    #post_dic = post.dict()
    #post_dic['id'] = randrange(0,100000)
    #my_post.append(post_dic)
    #return {"Data" : post_dic}
    #using sql now
    cursor.execute(""" INSERT INTO posts(title,content,is_published) VALUES(%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data : " : new_post}
    
# get individual post
@app.get("/posts/{id}")
def get_post(id : str):
    cursor.execute("""SELECT * FROM posts where id = %s """, (str(id),))
    post = cursor.fetchone()
    #print(post)
    
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f" post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f" post with id {id} not found")
    #print(post)
    return {"response" : post }

# delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    cursor.execute(""" DELETE FROM posts where id = %s RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#update post
@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, is_published = %s WHERE id = %s  RETURNING* """, (post.title, post.content, post.published, str(id)))
    updated_post= cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_post[index] = post_dict
    return {"Data ": updated_post}