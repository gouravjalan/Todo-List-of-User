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
@app.post("/Signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = crud.signup_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    if not new_user.roles:
        raise HTTPException(status_code=500, detail="Role not assigned properly")

    role = new_user.roles[0].role

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": role
    }

    #before 3rd table
    #return new_user

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

@app.post("/Login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    existing_user = crud.login_user(db, user)

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Ensure role exists
    if not existing_user.roles:
        raise HTTPException(
            status_code=400,
            detail=f"User has no role assigned (user_id={existing_user.id})"
        )

    role = existing_user.roles[0].role

    #below lines after making 3rd table 
    access_token = create_access_token({
        "sub": str(existing_user.id),
        "role": role
        }
    )

    refresh_token = create_refresh_token({
        "sub": str(existing_user.id)
        }
    )

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
# @app.get("/users/", response_model=list[schemas.UserResponse])
# def get_users(
#     db: Session = Depends(get_db)
#     ):
#     return crud.get_users(db)

#for rbac for all users
@app.get("/users/get_all_users", response_model=list[schemas.UserResponse])
def get_users(token:str, db: Session = Depends(get_db)):
    token_user = verify_token(token)

    if not token_user:
        raise HTTPException(status_code = 401, detail="Invalid token.")
    
    if token_user["role"] != "admin":
        raise HTTPException(status_code=403, detail= "Not authorized to access the data of all users.")
    
    #before 3rd table
    #return crud.get_users(db)

    #after table 3rd below lines
    users = crud.get_users(db)
    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.roles[0].role if u.roles else None
        }
        for u in users
    ]

#get single user on basis of id
@app.get("/users/get_single_user", response_model=schemas.UserResponse)
def get_user(user_id: str, token :str, db: Session = Depends(get_db)):
    token_user = verify_token(token)
    if token_user == "expire":
        raise HTTPException(status_code = 401,detail ="Token Expired.")
    
    if not token_user:
        raise HTTPException(status_code=401,detail="Invalid Token.")
    
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    #updated for rbac
    if str(user_id) != token_user["user_id"] and token_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to get the other users data.")
    
    #before 3rd table
    #return user

    #after 3rd table
    return{
        "id": user.id,
        "name":user.name,
        "email": user.email,
        "role": user.roles[0].role if user.roles else None
    }

#for soft delete
# @app.delete("/users/{user_id}")
# def delete_user(user_id:str, db:Session = Depends(get_db)):
#     deleted_user = crud.delete_user(db,user_id)
#     if not deleted_user:
#         return HTTPException(status_code=401,detail="User not found")
    
#     return {"message" : "User soft deleted successfully"}

# TODO ROUTES

#create todo list (authenticated)
@app.post("/users/create_todo_list", response_model=schemas.TodoResponse)
def create_todo(user_id: str, token:str, todo: schemas.TodoCreate, db: Session = Depends(get_db)):

    token_user = verify_token(token)

    if token_user == "expire":
        raise HTTPException(status_code = 401, detail="Token Expired.")
    
    if not token_user:
        raise HTTPException(status_code=401,detail="Invalid token.")
    
    #updated for rbac
    if user_id != token_user["user_id"] and token_user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Not authorized to create todo list of user.")
    
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
#without rbac
# @app.get("/todo list of users", response_model=list[schemas.TodoResponse])
# def get_user_todos(db: Session = Depends(get_db)):
#     return crud.get_user_todos(db)

#with rbac
@app.get("/todos/get_all_users_todos", response_model=list[schemas.TodoResponse])
def get_user_todos(token: str, db: Session = Depends(get_db)):
    token_user = verify_token(token)

    if not token_user:
        raise HTTPException(status_code = 401, detail="Invalid token.")
    
    if token_user["role"] != "admin":
        raise HTTPException(status_code=403, detail= "Not authorized to access the data of all users todo's.")
    
    return crud.get_user_todos(db)

#get todo by id  todo_id is id of todo_list table
@app.get("/todos/get_single_user_todo", response_model=schemas.TodoResponse, )
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
    
    #updated for rbac
    if str(todo.user_id) != token_user["user_id"] and token_user["role"] != "admin":
        raise HTTPException(status_code=403,detail="Not authorized")

    return todo

#update todo list
@app.put("/todos/update_todos", response_model=schemas.TodoResponse)
def update_todo(todo_id: str, token : str , todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    token_user = verify_token(token)

    #to check token expiry.
    if token_user == "expire":
        raise HTTPException(status_code = 401, detail = "Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    #for rbac only. If not then prefer updated at end.
    # updated = crud.update_todo(db,todo_id,todo)  #here the order in which we give parameters should be same as that in crud.py file function of update.
    # if not updated:
    #     raise HTTPException(status_code=404, detail="Todo not found")

    #after table 3rd
    existing = crud.get_todo(db,todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")

    #before and after table 3rd same part as it is
    #just change existing to updated before making of 3rd table
    #updated for rbac
    if str(existing.user_id) != token_user["user_id"] and token_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    #it is here bcoz we will update after the authorization not before authorization.
    updated = crud.update_todo(db, todo_id, todo)

    return updated

#delete todo list
@app.delete("/todos/delete_todos")
def delete_todo(todo_id: str, token: str, db: Session = Depends(get_db)):
    #validat the token
    token_user = verify_token(token)
    #check token expired or not.
    if token_user == "expire": 
        raise HTTPException(status_code = 401, detail = "Token Expired")
    
    if not token_user:
        raise HTTPException(status_code=401, detail="Invalid token")
    #check if resource exist

    # deleted = crud.delete_todo(db, todo_id)
    # if not deleted:
    #     raise HTTPException(status_code=404, detail="Todo not found")
    
    existing = crud.get_todo(db,todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")
    #updated for rbac

    #after 3rd table but before it just existing to deleted 
    if str(existing.user_id) != token_user["user_id"] and token_user["role"] != "admin":
        raise HTTPException(status_code = 403,detail= "Not Authorized")
    
    #after table 3rd only
    deleted = crud.delete_todo(db, todo_id)

    return {"message": "Todo soft deleted successfully"}


#after table 3rd created.
# @app.put("/admin/assign-role")
# def assign_role(user_id: str, role: str, token: str, db: Session = Depends(get_db)):

#     token_user = verify_token(token)

#     if token_user["role"] != "admin":
#         raise HTTPException(status_code=403, detail="Only admin can assign roles")

#     user_role = db.query(models.UserRole).filter(
#         models.UserRole.user_role_id == user_id
#     ).first()

#     if not user_role:
#         raise HTTPException(status_code=404, detail="User role not found")

#     user_role.role = role

#     db.commit()
#     db.refresh(user_role)

#     return {"message": f"Role updated to {role}"}
    

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
    

# Note : if we dont want to send the request with api then simply remove the lines from 238 to 243 from every api request. 