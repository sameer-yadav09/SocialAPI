
from fastapi import  Depends, FastAPI
from orjson import OPT_STRICT_INTEGER
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from . import models
from .routers import post,auth,user,vote 


#us3ed to create table 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# websites which can use our api will be put here.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], #which methods to allow like get or delete or update
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")  #testing
def test_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}

#-----------end points move to routers folder in their respective files ----------------

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router) 
app.include_router(vote.router) 




# 1. cd social/venv/scripts
# 2. activate.bat
# 3. cd study\api\Social
# 4. uvicorn app.main:app --reload