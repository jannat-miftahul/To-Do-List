from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from models import Users
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated
from database import SessionLocal

router = APIRouter()

bcrypt_context = CryptContext(schema=['bcrypt'], deprecated='auto')

class CreateUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str = 'user'  # Default role is 'user'

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
