from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
#from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+pymysql://username:password@localhost/todo_db"

engine = create_engine(DATABASE_URL)
#creates a db engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
#base class for all db models.

#SessionLocal = sessionmaker(bind=engine)

#sessionmaker --->> a function that creates databasae sessions
#session = a temp. connection with db to run the queries.
#session is use to talk to database.

#FastAPI ---->> Sessions  ---->> MySQL Database
#without session fastapi can't run database queries.

#database_url --->> tells python to connect to this url.

#DATABASE_URL = "mysql+pymysql://root:manager@localhost/todo_db"
# mysql  --->> is database type
#pymysql ---->> is python driver to connect MySQL
#root ------->> is username of MySQL
#manager ---->> is password
#localhost -->> is db server location
#todo_db ---->> the database name

#engine = create_engine(DATABASE_URL)
#engine ---->> a variable that acts as bridge between python and mysql
#create_engine() ---->> a function if sqlalchemy that create a connection between python and db.
#bind = engine ---->> helps sqlalchemy to know which database to connect with.