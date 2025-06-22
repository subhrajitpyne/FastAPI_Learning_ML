import os
from fastapi import FastAPI, Request
from models import *
from database import engine
from typing import *
from routers import auth,todos,admin,user
from fastapi.templating import Jinja2Templates

app: FastAPI = FastAPI()

base.metadata.create_all(bind=engine) #This will create sqlite databse and it only runs if todos.db does not exist.


#Testing first Simple templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

templates: object = Jinja2Templates (directory=TEMPLATE_DIR)
@app.get("/")
async def test(request: Request):
    return templates.TemplateResponse("home.html",{'request': request})



#Adding Router objects to main Routes
app.include_router(auth.router) #Routing the API

app.include_router(todos.router)

app.include_router (admin.router)

app.include_router (user.router)

#main.py is only to start the FastAPI and all other things should be routed through routers.