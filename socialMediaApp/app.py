from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import pydantic_models, sql_models
from .database import engine, get_db


sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI() # fast API instance

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


@app.get("/")
async def login():
    return {"message": "Welcome to My API!"}

#query() object creates the SQL query so we dont have to when we print(posts) it returns 'SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.create_at AS posts_create_at'. .all() returns the results represented by this _query.Query as a list. This results in an execution of the underlying SQL statement.
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(sql_models.Post).all()
    print(posts)
    return {"status": "success"}


# Retrieve all post from database.
@app.get("/posts", response_model=List[pydantic_models.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(sql_models.Post).all()
    return posts

# Create new post. 
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=pydantic_models.PostResponse)
async def create_post(post : pydantic_models.PostCreate, db: Session = Depends(get_db)):
    new_post = sql_models.Post(**dict(post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# client provide a path param 'id' to retrieve individual post. Path param passed SQL query, if not found raise http exception built in to fastapi, if found return post
@app.get("/posts/{id}", response_model=pydantic_models.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)): # validation: client can only pass int
    post = db.query(sql_models.Post).filter(sql_models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"post with id: {id} was not found"
            )
    return post


# delete individual post. Query for post with specific id. if it doesnt exist throw an error. if it does delete post and commit changes to db
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,  db: Session = Depends(get_db)): # validation: client can only pass int
    deleted_post = db.query(sql_models.Post).filter(sql_models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
            )
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update individual post. Query for post with specific id. if it doesnt exist throw an error. if it does chain update() method to found query and update post with passed in field from post. turn into dictionary with dict(post) and commit changes to db
@app.put("/posts/{id}", response_model=pydantic_models.PostResponse)
async def update_posts(id: int, post: pydantic_models.PostCreate, db: Session = Depends(get_db)): # validation: client can only pass int and post object
    post_query = db.query(sql_models.Post).filter(sql_models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist"
        )
    post_query.update(dict(post), synchronize_session=False)
    db.commit()
    return post_query.first()