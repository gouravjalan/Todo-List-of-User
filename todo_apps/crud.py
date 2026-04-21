from sqlalchemy.orm import Session #to run queries
import models
import schemas
from authorization import verify_password, hash_password
from sqlalchemy.orm import joinedload

#USER OPERATIONS
#sign up logic
def signup_user(db: Session, user: schemas.UserCreate,current_user):  #to signup if new user, and this is what api response should look like.

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if existing_user:
        return None

    hashed_password = hash_password(user.password)
    # converts normal password to hashed password and store it in db.

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        modified_by = current_user["user_id"],
        roles=[models.UserRole(
            role=user.role.lower(),
            modified_by = current_user["user_id"]  #token_user is your current_user just called with different name.
            )
        ]
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#login user without oauth2 authorization.
# def login_user(db: Session, user):

#     existing_user = (
#         db.query(models.User)
#         .options(joinedload(models.User.roles))   #THIS LINE FIXES YOUR ISSUE
#         .filter(models.User.email == user.email)
#         .first()
#     )

#     if not existing_user:
#         return None

#     # if existing_user.password != user.password:
#     #     return None
#     # existing_user.password -------> for hashed password
#     # user.passwored ---------------> still the plain password so it do not match with above and throws error.
    
#     if not verify_password(user.password,existing_user.password):
#         return None

#     return existing_user


#for oauth2 authorization 
def login_user(db: Session, form_data):

    existing_user = db.query(models.User).filter(
        models.User.email == form_data.username   # ✅ FIX
    ).first()

    if not existing_user:
        return None

    if not verify_password(form_data.password, existing_user.password):
        return None

    return existing_user


def get_user(db: Session, user_id: str):  #to fetch single user, that's y .filter is used(filter by id) with .first (returning the first occurrence)
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):  #to fetch all the users in db
    return db.query(models.User).all()


# todo OPERATIONS

def create_todo(db: Session, user_id: str, todo: schemas.TodoCreate, current_user):
    new_todo = models.Todo(   #create obj of new todo list
        title=todo.title,
        description=todo.description,
        user_id=user_id,
        is_deleted_check = False,
        modified_by = current_user["user_id"]
    )

    db.add(new_todo)  #add new todo list to db
    db.commit()   #save to database
    db.refresh(new_todo)  #reload db with new db data

    return new_todo

 # to fetch all todos that belongs to specific user.
def get_user_todos(db: Session):
    todos = db.query(models.Todo).all()  
   
    return todos


#to fetch single todo
def get_todo(db: Session, todo_id: str):
    return db.query(models.Todo).filter(
        models.Todo.id == todo_id, 
        models.Todo.is_deleted_check == False
        ).first()   


#to update the todo without oauth2 authorization
# def update_todo(db: Session, todo_id: str, todo: schemas.TodoUpdate):
#     existing_todo = db.query(models.Todo).filter(
#         models.Todo.id == todo_id,
#         models.Todo.is_deleted_check == False
#         ).first()  
   
#     if not existing_todo:
#         return None
    
#     existing_todo.completed = todo.completed #update status

#     db.commit()
#     db.refresh(existing_todo)
#     return existing_todo


#with oauth2 authorization
def update_todo(db: Session, todo_id: str, todo: schemas.TodoUpdate, current_user):

    existing_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if not existing_todo:
        return None

    existing_todo.completed = todo.completed
    existing_todo.modified_by = current_user["user_id"]

    db.commit()
    db.refresh(existing_todo)

    return existing_todo


def delete_todo(db: Session, todo_id: str):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    
    todo.is_deleted_check = True
                                
    db.commit() #save to db
    db.refresh(todo)

    return todo


#.query(models.Todo) ---->> is equivalent to select * from todo_list
#i.e is query the table todo_list in database.
#.filter ---->> is like a where clause in sql (condition)
#.all ---->> returns all the matching rows
#.first ---->> returns first matching rows.

#def is fun define
#db:Session ---->> allows to talk to database.
#db.add()/db.delete() ---->> are all sqlalchemy db commands that help to perform op on db.

#user: schemas.UserCreate ------------>>> this means that function expects user data in the format defined by session.
#i.e the json body that we r visible with on api is because of the format that we give in schemas.py

#schemas.UserCreate ----->>> represents the structure of user data.

#db.delete(todo) ----->> to delete that row of todo list
#db.commit() --------->> save to db


#models contains the database tables as class in python and rows as objects.
#schemas contains the input/output structure (API Body)

#return db.query(models.User).filter(models.User.id == user_id).first()
#db means i want to talk to database.
#.query(models.User) means start a query on table User.
#.filter(models.User.id == user_id) means filter out whose id == user_id 
#.first() returns the first occurrence

#so the meaning of above line is 
#SELECT * FROM users WHERE id = user_id ;