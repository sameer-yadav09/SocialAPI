

from fastapi import  Depends, Response,status, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas,oauth2
from ..database import  get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",   # used for common part of the url
    tags=['posts']     #used to categorize operations based on post and user on the swagger ui
)

#limit,skip and search are the query parameter used to add additional search features(use "%20" in url for "space" )
@router.get("/",response_model=List[schemas.PostOut])   #GET ALLL
def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int = 0, search : Optional[str] = ""):  #add "current_user: int = Depends(oauth2.get_current_user)" if i need users to log in to see all posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #use this to get posts made by user only (add above commented part to function parameter for it to work)
    print(search)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #maskes a querry
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post) #change default status code
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(post.dict())
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict()) #unpacks dictionary(**)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #used to return the last entry to user
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)#(Response-model is used to get dersired fields im output)
def get_post(id: int, db:Session = Depends(get_db)):   #, current_user: int = Depends(oauth2.get_current_user)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found" )
    #following is used if i want to fetch posts only made by user
    #if post.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    #print(current_user.email)
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()    #returns first row

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response("deleted",status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
