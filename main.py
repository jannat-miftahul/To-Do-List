from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from models import Todos
from typing import Annotated
from database import engine, SessionLocal
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

# Pydantic models for request validation
class Todo(BaseModel):
    id : int
    title : str
    description : str = Field(max_length=100)
    priority : int = Field(gt=0, lt=6)
    completed : bool

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = Field(default=None, max_length=100)
    priority: Optional[int] = Field(default=None, gt=0, lt=6)
    completed: Optional[bool] = None


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Read all to-dos
@app.get('/')
def read_todos(db : db_dependency):
    return db.query(Todos).all()

# Read specific to-do by ID
@app.get('/todo/{todo_id}')
def read_specific_todos(db : db_dependency, todo_id : int):
    specific_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if specific_todo is not None:
        return specific_todo
    else:
        raise HTTPException(status_code=404, detail='To do not found')

# Create a new to-do
@app.post('/create/')
def create_todos(db : db_dependency, new_todo : Todo):
    todo_model = Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
    
    return JSONResponse(status_code=201, content={'message' : 'To do created successfully'})

# Update an existing to-do
@app.put('/edit/{todo_id}')
def update_todo(db: db_dependency, todo_id: int, updated_todo: TodoUpdate):

    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail='To do not found')

    update_data = updated_todo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value) 

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'To do updated successfully'})
