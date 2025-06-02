from database import base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean#Datatypes in databse

class Users(base):
    __tablename__ = 'users'
    
    #columns
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)
    phone_number = Column(String)
class Todos(base):
    __tablename__ = 'todos'
    
    #Columns
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column (String)
    description = Column(String)
    priority = Column(Integer,default=1)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey('users.id'))

