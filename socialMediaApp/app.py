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


# Retrieve all post from server
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

# Create post, adds post to empty dict, adds unique id to post, appends new post to my post list. returns 201 created status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post):
    post_dict = dict(post)
    post_dict['id']= randrange(0 , 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# client provide a path param 'id' to retrieve individual post. Path param passed into find_post function, if not found raise http exception built in to fastapi, if found return post
@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = f"post with id: {id} was not found"
            )
    return {"post_details": post}


# delete individual post. Uses find index post function which returns the index of post with passed in id, if index exists pop index from my post list and return 204 response
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT, detail=f"post {id} successfully deleted")

# Update individual post. User send put request with the id for specifc post. We find the index of the post, if exists we Takes post from front end,convert to dictionary and assigns this post the id of the passed in id, then replace the post in my post lists with the new passed in post, then returns new post.
@app.put("/posts/{id}")
async def update_posts(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_dict = dict(post)
    post_dict['id']= id
    
    my_posts[index] = post_dict
    return {"data": post_dict}