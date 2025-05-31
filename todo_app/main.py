from fastapi import FastAPI
from models import *
from database import engine
from typing import *
from routers import auth,todos

app: FastAPI = FastAPI()

base.metadata.create_all(bind=engine) #This will create sqlite databse and it only runs if todos.db does not exist.

app.include_router(auth.router) #Routing the API

app.include_router(todos.router)

#main.py is only to start the FastAPI and all other things should be routed through routers.