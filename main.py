from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from models import Todos
from typing import Annotated
from database import engine, SessionLocal

app = FastAPI()

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
