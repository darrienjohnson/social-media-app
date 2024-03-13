from fastapi import FastAPI, Response, status, HTTPException
from curses.ascii import HT
from hashlib import new
from lib2to3.pytree import Base
from operator import imod, index
from pickle import NONE
from typing import Optional
from fastapi.params import Body
# data validation library used to define & validate data models simplying validation, parsing, & serialization task
from pydantic import BaseModel

from random import randrange

app = FastAPI() # fast API instance

# class defining the schema of what our front end data should look like
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #if user doesnt give value, default is True
    rating : Optional[int] = None

# temp storage for saving post
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

# Creates a function to find individual posts. If post in post array has id = to the id passed in the function, return post
def find_post(id):
    for p in my_posts:
        if p["id"] == id: # type of pass param is str but id in my_list is type int. Must convert
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Decorators are used to associate a Python function with a specific HTTP endpoint (URL path)
@app.get("/")
async def login():
    # data sent back to user making get request
    return {"message": "Welcome to My API!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post : Post): #extract all fields from body store in variable payLoad
    # Have to save post somewhere instead of just returning back to user
    # save post in memory in array ⬆️
    post_dict = post.dict()
    post_dict['id']= randrange(0 , 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}") # Path parameter for id of specific post
async def get_post(id: int): # type of passed param is str but id in my_list is type int. validation needed
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        # ------instead of this ⬆️ we can do this ⬇️
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return {"post_details": post}

    # delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    #find item specific index
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #my_posts.pop(index) removes it from the my_post array
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Put request to the specific id(post) they want to update
@app.put("/posts/{id}")
async def update_posts(id: int, post: Post):
    # find the index of that post using our find_index_post function from ⬆️
    index = find_index_post(id)
    # error handling if index not found
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    # if post exist take front end data (passed in data) and converts to dictionary
    post_dict = post.dict()
    # the newly created dictionary will give it an id of the desired post
    post_dict['id']= id
    # replace post at found index with new updated post
    
    my_posts[index] = post_dict
    return {"data": post_dict}