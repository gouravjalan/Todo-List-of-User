from pydantic import BaseModel #to validate api data.

# USER SCHEMAS

class UserCreate(BaseModel):   #during create user the 3 parameters should be used (request body)
    name: str
    email: str
    password: str

class UserResponse(BaseModel):  #defines what api returns & password is hidden for security
    id: str
    name: str
    email: str
    role: str

    # the below line allows to convert SQLAlchemy Object ---->> Pydantic Object
    class Config:
        from_attributes = True

class UserLogin(BaseModel):  #to login the user
    email: str
    password: str

class Token(BaseModel):   
    access_token : str   #this is type annotation
    token_type : str
    refresh_token : str

# TODO SCHEMAS

class TodoCreate(BaseModel): #during creating todo list of user the 2 parameters should be used (request body)
    title: str
    description: str

class TodoUpdate(BaseModel):  #Used for updating task status.(true/false only)
    completed: bool

class TodoResponse(BaseModel): #api response structure.
    id: str
    title: str
    description: str
    completed: bool
    user_id: str
    is_deleted_check: bool   #soft delete

    class Config:
        from_attributes = True



#from pydantic import BaseModel #to validate api data.
#pydantic is data validation library used for data validataion & parsing.
#BaseModel is base class used to create schemas in FastAPI, All schemas must inherit from FastAPI.
#pydantic model is python class that define structure of python class using type hints.