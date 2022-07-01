from typing import List
from .. import schema, models,util
from sqlalchemy.orm import Session
from ..database import get_db, engine
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter

router = APIRouter(
    prefix= "/users"
)




#View user
@router.get("/",response_model=List[schema.GetUser])
def user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

#create user
@router.post("/", response_model=schema.GetUser)
def create_user (user: schema.User,db: Session = Depends(get_db)):
    # to harsh password
    hashed_password = util.hash_pwd(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#get user
@router.get("/{id}", response_model=schema.GetUser )
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f" post with id {id} not found")
    return user