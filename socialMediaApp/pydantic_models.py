from sys import deactivate_stack_trampoline
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr
from datetime import datetime

from socialMediaApp.sql_models import Post

# Pydantic validates the received input data matches the expected data defined in the data model (schema). Schema/Pydatic Models define the structure of a request and response. This ensures clients request only valid if it contain title and content in body.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Pydantic's orm_modde will tell pydantic model to read the data even if it is not a dict but an ORM model (or any other arbitrary object with attributes) inherits title, content, and publish from base class
class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True