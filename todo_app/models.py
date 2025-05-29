from database import base
from sqlalchemy import Column, Integer, String, Boolean#Datatypes in databse

class Todos(base):
    __tablename__ = 'todos'
    
    #Columns
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column (String)
    description = Column(String)
    priority = Column(Integer,default=1)
    complete = Column(Boolean,default=False)