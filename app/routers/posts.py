from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#Retrieve All Posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int=10, skip: int=None, search: Optional[str]=''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

#Retrieve post by ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
            .join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True)\
            .group_by(models.Post.id)\
            .filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")  
    
    return post

#Create Post
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, location, published)
    #                VALUES (%s, %s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.location, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#Delete Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform the requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update a Post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post:schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts
    #                SET title=%s, content=%s, location=%s, published=%s
    #                WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.location, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform the requested action")
    
    # Convert Pydantic model to dictionary with exclude_unset=True
    update_data = post.dict(exclude_unset=True)  # Exclude fields not set in the request
    
    post_query.update(update_data, synchronize_session=False)
    db.commit()

    return post_query.first()