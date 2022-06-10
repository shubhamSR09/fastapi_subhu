import email
from fastapi import FastAPI
from uvicorn
import uvicorn
import py_functions
import config
import pyodbc
import json

app = FastAPI()

def connect_db(pwd):
    driver=config.DRIVER
    server = config.SERVER
    database = config.DATABASE
    uid= config.UID
    pwd = pwd 
    trust = config.TRUST
    con_string = config.TRUEST
    con_string = F'DRIVER={driver}; SERVER={server};DATABASE={database};UID={uid}; PWD={pwd}'
    cnxn=pyodbc.connect(con_string)
    cnxn.autocommit=True
    cursor = cnxn.cursor()
    print("Connection Successful with Database")
    return cnxn, cursor

    with open('SQL/password.json') as f:
        data = json.load(f)
    pwd = data['password']

    @app.get('/')
    def get_data(search:str = ""):
        df = py_functions.fetch_data(search,cnxn)
        return df.to_dict('r')

    @app.post('/singnup/')
    def signup(firstname: str, lastname:str, city:str, email:str, password:str):
        if '@gmail.com' not in email:
            return {"email ID Invalid"}
        user_exist = py_functions.check_user_exist(email,cnxn)
        if user_exist==0:
            singnup_query=py_functions.signup_data(firsname, lastname,city,email,password)
            cursor.execute(signup_query)
            return {"status":"signed UP Please login with same creds."}
        else:
            return{"status":'Email ID already exist.'}

    @app.post("/login/")
    def login(email: str, password:str):
        user_exist = py_functions.check_user_details(email,password,cnxn)
        if user_exist>0:
            return {"status","login Successful Access Granted"}
        else:
            return {"status","Login error Access not Granted"}

    if __name__ =="__main__":
        uvicorn.run(app, host="127.0.0.1", port=8000)