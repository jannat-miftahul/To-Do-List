from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from models import Users
from fastapi.responses import JSONResponse

router = APIRouter()

class CreateUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str = 'user'  # Default role is 'user'

@router.post('/create-user/')
def create_user(db : db_dependency, new_user : CreateUser):
    user_model = Users(
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        hashed_password=new_user.hashed_password,
        role=new_user.role
    )

    db.add(user_model)
    db.commit()
    
    return JSONResponse(status_code=201, content={'message' : 'User created successfully'})
