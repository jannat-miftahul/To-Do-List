from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from typing import Annotated
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter()

bcrypt_context = CryptContext(schema=['bcrypt'], deprecated='auto')

class CreateUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    
def authenticate_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if bcrypt_context.verify(password, user.hash_password):
        return user
    return False

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail='User not found')
        return {'username': username, 'id': user_id}
    except:
        raise HTTPException(status_code=404, detail='User not found')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Create a new user
@router.post('/create-user/')
def create_user(db : db_dependency, new_user : CreateUser):
    user_model = Users(
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        hashed_password=bcrypt_context.hash(new_user.password),
        role=new_user.role
    )

    db.add(user_model)
    db.commit()
    
    return JSONResponse(status_code=201, content={'message' : 'User created successfully'})

@router.post('/login')
def login_user(db : db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = authenticate_user(form_data.username, form_data.password, db) 
    if not user: 
        return "Failed authentication"
    
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}
