# from fastapi import FastAPI
# from app.db.database import Base, engine
# from app.routers import auth
# from fastapi.staticfiles import StaticFiles
# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = FastAPI()
# Base.metadata.create_all(bind=engine)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.include_router(auth.router)


from fastapi import FastAPI 

from routers import meetings
app.include_router(meetings.api)
