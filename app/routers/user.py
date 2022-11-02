from typing import List
from .. import schema, models,util
from sqlalchemy.orm import Session
from ..database import get_db, engine
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import oauth2

router = APIRouter(
    prefix= "/users",
    tags = ['Users']
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


#update user profile
@router.put("/{id}", response_model=schema.GetUser)
#@router.put("/{id}")
def update_post(id: int, updated_user:schema.UserBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print (updated_user)
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"{id} not found")
    

    if user.id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to perform such action")

    user_query.update(updated_user.dict(), synchronize_session = False)
    db.commit()

    print (user)
    return user
    #return {"Message" : "Testing is real"}


  