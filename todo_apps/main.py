from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal #imports database connection
from authorization import create_access_token,verify_token
from authorization import create_refresh_token      

import models
import schemas
import crud

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#api instance

# DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# USER ROUTES

#sign up
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = crud.signup_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return new_user

#to login ----->>> this code before use of jwt
# @app.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

#     existing_user = crud.login_user(db, user)

#     if not existing_user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     return {"message": "Login successful",
#             "user_id" : existing_user.id
#     }


#this is login part when using jwt login
# this for earlier when json format 

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    existing_user = crud.login_user(db, user)

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # create jwt token
    access_token = create_access_token(data={"sub": str(existing_user.id)})

    refresh_token = create_refresh_token(data={"sub" : str(existing_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

#an api for a refresh token
# @app.post("/Refresh")
# def refresh_token(refresh_token:str):
#     user_id = verify_token(refresh_token)

#     if not user_id:
#         raise HTTPException(status_code=401,detail="Invalid Refresh Token")
    
#     new_access_token = create_access_token(data={"sub" : user_id})

#     return{ "refreshed_access_token" : new_access_token }


#create user is not used bcoz signup is providing the same functionality as it.
"""
#create user
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

"""

#get all user
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db)
    ):
    return crud.get_users(db)

#get single user on basis of id
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: str, token :str, db: Session = Depends(get_db)):
    token_user = verify_token(token)
    if token_user == "expire":
        raise HTTPException(status_code = "Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401,detail="Invalid Token")
    
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if str(user_id).strip() != str(token_user).strip():
        raise HTTPException(status_code=403, detail="Not authorized")
    return user


#for soft delete
# @app.delete("/users/{user_id}")
# def delete_user(user_id:str, db:Session = Depends(get_db)):
#     deleted_user = crud.delete_user(db,user_id)
#     if not deleted_user:
#         return HTTPException(status_code=401,detail="User not found")
    
#     return {"message" : "User soft deleted successfully"}

# TODO ROUTES

#create todo list (authenticated)
@app.post("/users/{user_id}/todos/", response_model=schemas.TodoResponse)
def create_todo(user_id: str, token:str, todo: schemas.TodoCreate, db: Session = Depends(get_db)):

    token_user = verify_token(token)

    if token_user == "expire":
        raise HTTPException(status_code = 401, detail="Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401,detail="Invalid token")
    
    if user_id != token_user:
        raise HTTPException(status_code=403,detail="Not authorized")
    
    return crud.create_todo(db, user_id, todo)

#get all todo of user
# the below code uses both token and id to get the user which means that it's working is same as that of get a single todo list.
# def get_user_todos(user_id: str, token: str,  db: Session = Depends(get_db)):
    # token_user = verify_token(token)
    # if not token_user:
    #     raise HTTPException(status_code=401,detail="Invalid token")
    
    # if user_id != token_user:
    #     raise HTTPException(status_code=403,detail="Not authorized")
    
    # return crud.get_user_todos(db, user_id)

#to get todos of all users at once (whole)
@app.get("/todo list of users", response_model=list[schemas.TodoResponse])
def get_user_todos(db: Session = Depends(get_db)):
    return crud.get_user_todos(db)

#get todo by id  todo_id is id of todo_list table
@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse, )
def get_todo(todo_id: str, token :str, db: Session = Depends(get_db)):
    token_user = verify_token(token)

    #check token expired or not.
    if token_user == "expire":
        raise HTTPException(status_code = 401, detail = "Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401,detail="Invalid token")
    
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if str(todo.user_id) != token_user:
        raise HTTPException(status_code=403,detail="Not authorized")

    return todo

#update todo list
@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: str, token : str , todo: schemas.TodoUpdate, db: Session = Depends(get_db)):

    token_user = verify_token(token)

    
    #to chech token expiry.
    if token_user == "expire":
        raise HTTPException(status_code = 401, detail = "Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    updated = crud.update_todo(db, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")

    if str(updated.user_id) != token_user:
        raise HTTPException(status_code=403, detail="Not Authorized")
    return updated

#delete todo list
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str, token: str, db: Session = Depends(get_db)):
    #validat the token
    token_user = verify_token(token)

    #check token expired or not.
    if token_user == "expire":
        raise HTTPException(status_code = 401, detail = "Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401, detail="Invalid token")
   
    #check if resource exist
    deleted = crud.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    #check ownership
    if str(deleted.user_id) != token_user:
        raise HTTPException(status_code = 403,detail= "Not Authorized")
    
    return {"message": "Todo soft deleted successfully"}

    

#todo_id is id of todo_list tablea


#models.Base.metadata.create_all(bind=engine)
#models ---->> means import database tables
#Base ------>> parent class for all db methods
#metadata -->> collection of all tables definition
#create_all() -->> checks if table is present in db or not, if not then create it.
#engine ------->> is db connection.

"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() #runs after each api request finishes.

"""
# get_db ---->>a function to create db session and provide it to api endpoint.
#try  ---->> to try a block of code in exception handling.
#yield --->> its like a vending machine which resumes from where it stopped instead of starting again.
#finally  --->> runs no matter what

#try,finally are majorly used in exception handling 

#@app.get("/users/", response_model=list[schemas.UserResponse])
#@ represents a decorator
#@app.get("/users/") tells fastapi to create a api route thats responds to GET request.
#/users/ ---->>> it is api path    so the full endpoint is #http://127.0.0.1:8000/users/#
#response_model ---->>> it controls what data you api should return/send back
#so here we just wanted to get response in a format which is inside schemas.py and the response should be in form of a list.


#def create_user(user: schemas.UserCreate, db: Session = Depends(get_db))
#Call get_db() first and pass the database session to db

# create_user is a function.
#user data shoud have a data format as in UserCreate of schemas.py 
#Depends(get_db)   --->>> is fastapi dependency injection, before running this function call get_db() and provide db session to talk.
#Depends   --->> a function usef for dependency injection, 
#this tells fastapi to run another function and provide it's result to your api function 



#this steps in every api are added to send a token with each requests to api for validation
#validat the token
    # token_user = verify_token(token)
    # if not token_user:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    #  #check ownership
    # if str(deleted.user_id) != token_user:
    #     raise HTTPException(status_code = 403,detail= "Not Authorized")
    

# NOTE : if we dont want to send the request with api then simply remove the lines from 238 to 243 from every api request. 