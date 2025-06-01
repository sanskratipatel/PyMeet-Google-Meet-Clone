
# app = FastAPI()
# Base.metadata.create_all(bind=engine)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.include_router(auth.router)


from fastapi import FastAPI 

from routers import meetings
app.include_router(meetings.api)
