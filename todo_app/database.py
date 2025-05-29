from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Database URL
SQLALCHEMY_DB_URL: str = "sqlite:///./todos.db"

#Database Engine
engine: create_engine = create_engine(url=SQLALCHEMY_DB_URL,
                                      connect_args={'check_same_thread':False})

#Session of the database to do CRUD operations
session_local: sessionmaker = sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=engine)

#This is the object of the database which we are going to use
base: declarative_base = declarative_base()