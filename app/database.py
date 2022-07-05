from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/Social'
                            
#we will use environment variables instead of hardcoding the url to prevent our sensitive info from leaking.

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()  

def get_db():  #creates session for every requests
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
