from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from . database import get_db
from . import models
from . import schema
from .config import settings


oauth_schema =  OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute

def create_token(data : dict):
    to_encode = data.copy()
    expire  =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    just_encode = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    #Token = jwt.encode({'key': 'value'}, 'secret', algorithm='HS256')
    return just_encode

#jwt.decode(token, 'secret', algorithms=['HS256'])
#{u'key': u'value'}

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None :
            raise credentials_exception
        token_data =schema.GetToken(id=id)
    except JWTError as e:
        raise credentials_exception
 
    
    return token_data
    
def get_current_user(token:str = Depends(oauth_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate Credentials", headers={"WWW-Authenticate": "bearer"})
    
    token = verify_token(token, credentials_exception)  
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user