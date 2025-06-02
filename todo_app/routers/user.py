from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from models import *
from database import session_local
from sqlalchemy.orm import Session
from typing import *
from starlette import status
from typing import *
from models import Users
from database import session_local
from sqlalchemy.orm import Session
from routers.auth import bcrypt_context,get_current_user
#from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer #This class is used in FastAPI to help you and Bearer token
#handle login forms that follow the OAuth2 password flow.
#from jose import jwt,JWTError


router: APIRouter = APIRouter(
    prefix='/user',
    tags=['user']
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


@router.get('/info', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(current_user: user_dependancy, db: db_dependancy):  # type: ignore
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')

    # ✅ Filter by ID from the JWT payload
    user = db.query(Users).filter(Users.id == current_user.get('id')).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


#Reset Password
@router.post('/reset_password', status_code=status.HTTP_202_ACCEPTED)
async def reset_password(password: str,
                         current_user: user_dependancy,  # type: ignore
                         db: db_dependancy) -> object:  # type: ignore

    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')

    user = db.query(Users).filter(Users.id == current_user['id']).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user.hashed_password = bcrypt_context.hash(password)

    db.add(user)
    db.commit()

    return {"message": "Password has been updated successfully."}
        
    
    


