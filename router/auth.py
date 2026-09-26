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