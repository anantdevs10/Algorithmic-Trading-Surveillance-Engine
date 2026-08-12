from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# SETS UP THE SQLAlchemy engine and a session factory pointed at the local SQLite file.
# Every router will import SessionLocal to talk to the DB.
DATABASE_URL = "sqlite:///./ats.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''
Setting up the SQLAlchemy Database we will be using for this project. 
SessionLocal is module where isolated database sessions can be created for database transactions
Base is an ORM Base which is a parent class for database models/tables/ 
Get_db opens a database session  when an incoming HTTP Request comes through. 
Using try and finally, when the http request is completed the database closes preventing memory leaks or leaks. 
'''