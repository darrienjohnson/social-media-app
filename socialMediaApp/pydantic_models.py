from pydantic import BaseModel

from socialMediaApp.sql_models import Post

# Pydantic validates the received input data matches the expected data defined in the data model (schema). Schema/Pydatic Models define the structure of a request and response. This ensures clients request only valid if it contain title and content in body.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
