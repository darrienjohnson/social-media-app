from sqlalchemy import text
from email import contentmanager
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# models represent tables to be created in the database
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content =  Column(String, nullable=False)
    published =  Column(Boolean, server_default='True', nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__= "users"