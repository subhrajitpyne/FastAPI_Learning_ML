from fastapi import APIRouter,Depends, Query,HTTPException
from pydantic import BaseModel, Field
from models import *
from database import session_local
from sqlalchemy.orm import Session
from typing import *
from starlette import status
from routers.auth import get_current_user
from typing import *
from models import Users
from passlib.context import CryptContext
from database import session_local
from sqlalchemy.orm import Session
from routers.auth import bcrypt_context
#from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer #This class is used in FastAPI to help you and Bearer token
#handle login forms that follow the OAuth2 password flow.
#from jose import jwt,JWTError


router: APIRouter = APIRouter(
    prefix='/admin',
    tags=['admin']
)

#DB query Generator as we have used yield here.
def get_db():
    db: object = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependancy: Callable = Annotated[Session, Depends(get_db)] #Made this typing annotation as variable so that
#We do not need to use this long call with every CRUD api
user_dependancy: Callable = Annotated[dict,Depends(get_current_user)] #Authorization of APIs Dependancy injection
# @router.get("/")
# async def read_all(db: Annotated[Session, Depends(get_db)]):

@router.get("/todos",status_code=status.HTTP_200_OK)
async def read_all(db: db_dependancy, # type: ignore
                   user: user_dependancy): # type: ignore
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Login failed...')
    
    return db.query(Todos).all()




class CreateUserRequest(BaseModel):
    username: str 
    password: str
    first_name: str
    last_name: str
    email: str
    role: str
    phone_number: str
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    username: str
    #hashed_password: str
    first_name: str
    last_name: str
    email: str
    role: str
    phone_number: str | None

    class Config:
        orm_mode = True

#Create User
@router.post("/create_user",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(current_user:user_dependancy, # type: ignore
                      db:db_dependancy, # type: ignore
                      create_user: CreateUserRequest) -> dict: # type: ignore
    
    if current_user is None or current_user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Only Admin can create user...')
    user: Users = Users(
        username = create_user.username,
        hashed_password = bcrypt_context.hash(create_user.password),
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        email = create_user.email,
        role = create_user.role,
        phone_number = create_user.phone_number
    )
    
    if user:
        db.add(user)
        db.commit()
        return user
    raise HTTPException(status_code=401,detail = "User was not created")

#Gaet all user data
@router.get('/all_users',response_model=list[UserResponse],status_code=status.HTTP_200_OK) #as we are having multiple users thus response model
#must be a list of Userresponse models thus list[UserResponse] ...
async def get_all_user(current_user: user_dependancy, # type: ignore
                       db: db_dependancy) -> dict: # type: ignore
    
    if current_user is None or current_user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Only Admin can create user...')
    
    return db.query(Users).all()

#Delete User
@router.delete('/delete_user',status_code=status.HTTP_202_ACCEPTED)
async def delete_user(current_user: user_dependancy, # type: ignore
                       db: db_dependancy, # type: ignore
                       username: str) -> dict:
    
    if current_user is None or current_user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Only Admin can create user...')
    
    user: Users = db.query(Users).filter(Users.username == username).first()
    
    if user:
        db.delete(user)
        db.commit()
        #return {'message': 'Todo has been deleted...'}
    else:
        raise HTTPException(status_code=404,detail=f'User does not exist with username {username}')