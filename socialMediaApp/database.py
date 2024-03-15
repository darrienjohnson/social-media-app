from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-adress/hostname>/<databasae_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Taylor01@localhost/FastAPIDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function manages database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()