import os 
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessiomaker, declarative_base 
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status 

load_dotenv() 

DATABASE_URL =os.getenv("DATABASE_URL") 

if not DATABASE_URL:
    raise RuntimeError("Database Url is not set in .env" ) 

engine = create_engine( 
    DATABASE_URL, 
    connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {} 

) 
SessionLocal = sessiomaker(autocommit =False, autoflush = False , bind = engine) 
Base = declarative_base() 

def get_db():
    db = SessionLocal() 
    try: 
        yield db
    except Exception as e: 
        print(f"Database Error : {e}") 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR , detail = "DB Connection failed") 
    finally: 
        db.close() 
        