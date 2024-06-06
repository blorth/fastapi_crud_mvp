from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth, cache, dependencies

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Post, summary="Create Post", description="Create a new post.")
def create_post(post: schemas.PostCreate, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    """
    Create a new post for the authenticated user.
    """
    user = auth.get_current_user(db, token)
    return crud.create_post(db, post, user.id)

@router.get("/", response_model=List[schemas.Post], summary="Get Posts", description="Get all posts for the authenticated user.")
def read_posts(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    """
    Retrieve all posts for the authenticated user.
    """
    user = auth.get_current_user(db, token)
    if user.email in cache.cache:
        return cache.cache[user.email]
    posts = crud.get_posts_by_user(db, user.id)
    cache.cache[user.email] = posts
    return posts

@router.delete("/{post_id}", response_model=schemas.Post, summary="Delete Post", description="Delete a post by its ID.")
def delete_post(post_id: int, token: str = Depends(auth.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    """
    Delete a post by its ID for the authenticated user.
    """
    user = auth.get_current_user(db, token)
    post = crud.get_post(db, post_id)
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    crud.delete_post(db, post_id)
    return post
