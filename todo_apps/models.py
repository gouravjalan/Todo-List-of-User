from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship #to create relation between tables
from database import Base #base class from database file
import uuid
# from sqlalchemy import Integer
from sqlalchemy import Enum

class User(Base):  #base is inherited here.
    __tablename__ = "users"  #should match with db table name.

    # id = Column(Integer, primary_key=True, index=True) #index=true to make search faster
    id = Column(String(36), primary_key=True,index=True,default=lambda: str(uuid.uuid4()))
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(Enum("user","admin"), default = "user")
    todos = relationship("Todo", back_populates="user") 
    #1 user cann have multiple todo list


class Todo(Base):
    __tablename__ = "todo_list"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(String(36), primary_key=True,index=True,default=lambda: str(uuid.uuid4()))
    title = Column(String(255))
    description = Column(String(255))
    completed = Column(Boolean, default=False)
    user_id = Column(String(36), ForeignKey("users.id")) #todo_list.user_id ===>>> users.id
    is_deleted_check = Column(Boolean,default=False)

    user = relationship("User", back_populates="todos")
    #connects todo back to user
    # it allows to connect objects in python just like foreign keys in sql.
    #backpopulates ---->> links tow relationships together(<--->)

#basically models.py will have the basic details of database structure and it's table content.
#Column() is function ----->>>  Column(datatype, options) is syntax

#from sqlalchemy.orm import relationship
#relationship is function in sqlalchemy.orm
#sqlalchemy.orm allows user to work with db tables using python class instead of sql query.
# database table ----->> python class
#database rows ------->> python objects.

#we have made use of uuid here which hae type uuid4(), instead of using normal id concept,  we have used uuid which is hard to debug and so that the user data will be safe.
#uuid4 version is most commonly used as it generates a random number every time it executes and it is 128 bits wide which means single char can have 128 different combo's which is very hard to debug and get the info.
#so for this reason uuid4 is used here.

#default=lambda: str(uuid.uuid4())
# default means use this value if user dont provide any.
#lambda is function which here means the run this code every time a new row is created.
#id = str(uuid.uuid4()) helps to generate the id automatically when it is not provided by user.