from fastapi import FastAPI, Depends, HTTPException
import models
from models import Todos
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
