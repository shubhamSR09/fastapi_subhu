import email
from http.client import HTTPException
from fastapi import Depends, FastAPI 
from typing import List
from database import Base, SessionLocal, engine
from main1 import User
from models import Users
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from pydantic import BaseModel 


Base.metadata.create_all(bind=engine)


app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserSchema(BaseModel):
    id:int
    name:str
    email:str
    class Config:
        orm_mode=True

class UserCreateSchema(UserSchema):
    password:str

@app.get("/users", response_model=List[UserCreateSchema])
def get_users(db:Session =Depends(get_db)):
    return db.query(Users).all()

@app.post("/users", response_model=UserSchema)
def get_users(user:UserCreateSchema,db:Session =Depends(get_db)):
    u=Users(name=user.name,email=user.email,password=user.password)
    db.add(u)
    db.commit()
    return u


@app.put("/users/{user_id}",response_model=UserSchema)
def update_use(user_id:int,user:UserSchema,db:Session=Depends(get_db)):
    try:
        u=db.query(Users).filter(Users.id==user_id).first()
        u.name=user.name
        u.email=user.email
        db.add(u)
        db.commit()
        return u
    except:
        return HTTPException(status_code=404,detail="user not found")


@app.delete("/users/{user_id}", response_class=JSONResponse)
def detele_user(user_id:int,db:Session=Depends(get_db)):
    try:
        u=db.query(Users).filter(Users.id==user_id).first()
        db.delete(u)
        db.commit()
        return {f"user of id {user_id} has been deleted ":True}

    except:
        return HTTPException(status_code=404,detail="user not found")
