from datetime import datetime, timedelta, timezone
from fastapi import APIRouter,Depends, HTTPException
from starlette import status
from pydantic import BaseModel,EmailStr, Field,field_validator
import re
from typing import *
from models import Users
from passlib.context import CryptContext
from database import session_local
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer #This class is used in FastAPI to help you and Bearer token
#handle login forms that follow the OAuth2 password flow.
from jose import jwt,JWTError



router: APIRouter = APIRouter(
    prefix ='/auth',
    tags =['auth']
) #We are creting group in route for Swagger /docs

#Once User will be validated then the JWT token will be returned
SECRET_KEY:str = 'c352d3910388cdcfbd39c507135675c893855c30e57efa344bc93a41fe9a38d3' #openssl rand -hex 32
ALGORITHM: str = 'HS256'
#These will make JWT signature
#For each JWT we need algorith and secrert key
#Password Hashing
bcrypt_context:CryptContext = CryptContext(schemes=['bcrypt'],deprecated='auto')
#Creating dependancy for all other APIs
oauth2_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer (tokenUrl='/auth/token')



#DB query Generator as we have used yield here.
def get_db():
    db: object = session_local()
    try:
        yield db
    finally:
        db.close()
#DB dependancy injection
db_dependancy: Callable = Annotated[Session, Depends(get_db)] #Made this typing annotation as variable so that

#ValidationModel
class CreateUserRequest(BaseModel):
    username: str 
    password: str
    first_name: str
    last_name: str
    email: str
    role: str
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    email: str
    role: str

    class Config:
        orm_mode = True

#JWT token creation and encoding
# def create_access_token(username: str, id: int, expires_delta: timedelta) -> object: #Timedelta is needed to set token expire time
#     encode: dict = {'sub': username,'id': id}
#     expires: datetime = datetime.now(timezone.utc)
    
#     encode.update({'exp': expires})
    
#     return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)



def create_access_token(username: str, id: int, expires_delta: timedelta) -> str:
    to_encode: dict = {'sub': username, 'id': id}
    expire: datetime = datetime.now(timezone.utc) + expires_delta  # ✅ Correct usage else as soon as token will be genaratred, it will be expired
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



#****Creating a sync function to validate JWT token so that we can use it to authorize user to use APIs****
# async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]) -> object:
#     try:
#         payload: object = jwt.decode (token,SECRET_KEY,algorithms=ALGORITHM)
#         username: str = payload.get('sub')
#         id: int = payload.get('id')
#         if username is None or id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Login failed')
        
#         return {'username': username, 'id': id}
    
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Login failed')


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> object:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print("📥 Decoded JWT payload:", payload)  # 👈 Add this line

        username = payload.get('sub')
        id = payload.get('id')

        if username is None or id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login failed')

        return {'username': username, 'id': id}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login failed')

    
    
    
    
@router.post("/create_user",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy,create_user: CreateUserRequest) -> dict: # type: ignore
    user: Users = Users(
        username = create_user.username,
        hashed_password = bcrypt_context.hash(create_user.password),
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        email = create_user.email,
        role = create_user.role
    )
    
    if user:
        db.add(user)
        db.commit()
        return user
    raise HTTPException(status_code=401,detail = "User was not created")


def authenticate_user(username: str,password: str, db: Session) -> object:
    user: Users = db.query(Users).filter(Users.username == username.lower()).first()
    if not user:
        return False
    #bcrypt is macthing password and hashed password
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user
    
    #return True
        

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/token",response_model=Token,status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependancy) -> object: # type: ignore
    user:Users = authenticate_user(form_data.username,form_data.password,db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Login failed')
    
    token: object = create_access_token (user.username,user.id,timedelta(minutes=20)) #Token will be valid till 20 minutes
    #return {'username': f"{form_data.username} has been autehticated successfully...Token:{token}"}
    return {'access_token': token,'token_type': 'bearer'}

    