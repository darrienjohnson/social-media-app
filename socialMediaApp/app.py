from http.client import ImproperConnectionState
from fastapi import FastAPI, Response, status, HTTPException, Depends
from curses.ascii import HT
from hashlib import new
from lib2to3.pytree import Base
from operator import imod, index
from pickle import NONE
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from random import randrange
from sqlalchemy.orm import Session
import time
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI() # fast API instance


# Pydantic validates the received input data matches the expected data defined in the data model (schema).
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Psycopg2 enables use of PostgreSQL databases in application. Cursor object allows you to execute SQL commands against a PostgreSQL database.
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastAPIDatabase', user='postgres', password='Taylor01', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3)

# temp list storage for saving post
my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favorite foods",
        "content": "i like pizza",
        "id": 2
    }
 ]

# For post in my posts list, if post has id = passed in id param, return post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# For post in my post list, if post has id = passed in id param, return index of post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def login():
    return {"message": "Welcome to My API!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    db.query(models.Post).all()

    return {"status": "success"}


# Retrieve all post from database. Cursor object allows you to execute SQL commands against a PostgreSQL database. All rows from posts table selected. Fetchall() retrieves all the rows selected above, then return data
@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {"data": posts}

# Create new post. For data modification operations (INSERT, UPDATE, DELETE) use RETURNING to  modified data. INSERT statement to insert new post into the "posts" table. The values for the post's title, content, and published status are provided as parameters using %s placeholders in the SQL query. The RETURNING * used to retrieve the newly inserted post from the database after insertion. INSERT statement fetches the newly inserted post from the database using the fetchone() method. fetchone() retrieves the next row of a query result set as a single tuple. conn.commit() saves the transaction to the database.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):  # validation: client can only pass post object
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# client provide a path param 'id' to retrieve individual post. Path param passed SQL query, if not found raise http exception built in to fastapi, if found return post
@app.get("/posts/{id}")
async def get_post(id: int): # validation: client can only pass int
    cursor.execute("""SELECT * FROM posts WHERE id = %s; """, str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"post with id: {id} was not found"
            )
    return {"post_details": post}


# delete individual post. Uses find index post function which returns the index of post with passed in id, if index exists pop index from my post list and return 204 response. For (INSERT, UPDATE, DELETE) use commit() to save transaction to database.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int): # validation: client can only pass int
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *; """, str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update individual post. client request id for specifc post, pass updated values in SQL query with specifc up. For (INSERT, UPDATE, DELETE) use commit() to save transaction to database. then returns new post.
@app.put("/posts/{id}")
async def update_posts(id: int, post: Post): # validation: client can only pass int and post object
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": updated_post}