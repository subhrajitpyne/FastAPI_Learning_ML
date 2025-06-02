from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#***SQLAlchemy can not update table but we need to create new db if we want to add new tables

#Database URL
#SQLALCHEMY_DB_URL: str = "sqlite:///./todosapp.db" #sqlite

SQLALCHEMY_DB_URL: str = "mysql+pymysql://root:Admin098!@127.0.0.1:3306/todoapplicationdatabase" #mysql

#Database Engine
#engine: create_engine = create_engine(url=SQLALCHEMY_DB_URL,
                                      #connect_args={'check_same_thread':False}) #sqlite

engine: create_engine = create_engine(url=SQLALCHEMY_DB_URL)

#Session of the database to do CRUD operations
session_local: sessionmaker = sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=engine)

#This is the object of the database which we are going to use
base: declarative_base = declarative_base()