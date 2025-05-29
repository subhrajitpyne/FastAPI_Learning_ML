from fastapi import FastAPI,Depends, Query,HTTPException
from models import *
from database import engine,session_local
from sqlalchemy.orm import Session
from typing import *
from starlette import status

app: FastAPI = FastAPI()

base.metadata.create_all(bind=engine) #This will create sqlite databse and it only runs if todos.db does not exist.

#DB query Generator as we have used yield here.
def get_db():
    db: object = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependancy: Callable = Annotated[Session, Depends(get_db)] #Made this typing annotation as variable so that
#We do not need to use this long call with every CRUD api

# @app.get("/")
# async def read_all(db: Annotated[Session, Depends(get_db)]):
#     return db.query(Todos).all()

@app.get("/")
async def read_all(db: db_dependancy): # type: ignore
    return db.query(Todos).all()

@app.get("/todos/id/",status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependancy,id: int = Query(...,gt=0,description='TodoID')) -> dict:# type: ignore
    todo: Todos = db.query(Todos).filter(Todos.id == id).first()
    
    if todo is not None:
        return {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "priority": todo.priority,
            "complete": todo.complete
        }
    
    """
        You're returning a SQLAlchemy model (Todos), and FastAPI tries to encode it to JSON.

        But here's the catch:

        FastAPI (using Pydantic v2+) can't serialize ORM models directly unless orm_mode is used.
        Thus u need to return each datamember in a dictionary format
    """
    raise HTTPException(status_code=404,detail = "Todo not found")

#Creating schema for HTTP POST to validate the data
from pydantic import BaseModel,Field

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,max_length=100)
    priority: int = Field(ge=1,le=5,default=1)
    complete: bool = Field(default=False)
    class Config:
        orm_mode = True  # ✅ Important for SQLAlchemy integration
#Validate the response data
class TodoResponse(BaseModel):
    id: int
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,max_length=100)
    priority: int = Field(ge=1,le=5,default=1)
    complete: bool = Field(default=False)
    class Config:
        orm_mode = True  # ✅ Important for SQLAlchemy integration

@app.post("/todos/",status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependancy, todo_request: TodoRequest) -> dict: # type: ignore
    todo: Todos = Todos(**todo_request.model_dump())
    db.add(todo)
    db.commit()
    return {'message': 'Todo created...'}

@app.put("/todos/update_by_id",status_code=status.HTTP_202_ACCEPTED)
async def update_todo_by_id(db: db_dependancy,todo_request: TodoRequest,id: int=Query(...,gt=0,le=5)) -> dict:# type: ignore
     todo: Todos = db.query(Todos).filter(Todos.id == id).first()
     if todo:
         todo.title = todo_request.title
         todo.description = todo_request.description
         todo.priority = todo_request.priority
         todo.complete = todo_request.complete
         
         db.add(todo)
         db.commit()
         return {'message': 'Todo has been updated...'}
     raise HTTPException(status_code=404,detail='Todo not found with id')


@app.delete('/todos/delete/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db: db_dependancy,id: int=Query(...,gt=0,le=5)) -> None:# type: ignore
    todo: Todos = db.query(Todos).filter(Todos.id == id).first()

    if todo:
        db.delete(todo)
        db.commit()
        #return {'message': 'Todo has been deleted...'}
    else:
        raise HTTPException(status_code=404,detail='Todo not found with id')
        
    
        