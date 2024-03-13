from fastapi import FastAPI, Response, status, HTTPException
from curses.ascii import HT
from hashlib import new
from lib2to3.pytree import Base
from operator import imod, index
from pickle import NONE
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange

app = FastAPI() # fast API instance

# Pydantic validates the received input data matches the expected data defined in the data model (schema).
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

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

# Creates a function to find individual posts. For post in posts, if post in posts list has id = id argument return post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def login():
    return {"message": "Welcome to My API!"}

# Create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):
    post_dict = dict(post)
    post_dict['id']= randrange(0 , 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# Retrieve all post from server
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# client provide a path param 'id' to retrieve individual post. Path param passed into find_post function, if not found raise expection, if found return post
@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post_details": post}


# delete individual post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update individual post
@app.put("/posts/{id}")
async def update_posts(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = dict(post)
    post_dict['id']= id
    
    my_posts[index] = post_dict
    return {"data": post_dict}