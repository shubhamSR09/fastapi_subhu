from database import Base
from sqlalchemy import Column, Integer,String


class Users(Base):
    __tablename__="user_tb"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50))
    email=Column(String(100),unique=True)
    password=Column(String(100))