from typing import List, Optional
from .. import schema, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db, engine
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter

router = APIRouter(
    prefix= "/posts",
    tags = ['Post']
)

# get all post
@router.get("/", response_model=List[schema.PostVote])
#@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print (result)    
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #to get spefic post by a user
    #post_user = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 
    return result


# create a new post
@router.post("/", response_model=schema.Post)
#def posts(post : schema.CreatePost, db: Session = Depends(get_db)):
def posts(post : schema.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#This enable to ensure user log in inorder to post  user_id: int = Depends(oauth2.get_current_user)
#     #print (post.dict())
    #new_post = models.Post(title=post.title, content=post.content, published = post.published)
    #print (current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




# get individual post
@router.get("/{id}", response_model=schema.PostVote)
def get_post(id : int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()    
    if not post:
     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f" post with id {id} not found")
   
    return post

# delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post =  post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    #to check for ownership
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform such action")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#update post
@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post:schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id = %s  RETURNING* """, (post.title, post.content, post.published, str(id)))
    # updated_post= cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    # post.update({'title':'Updated Title','content':'Updated conted'}, synchronize_session = False)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform such action")

    post_query.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    print(post_query.first())
    return  post_query.first()
