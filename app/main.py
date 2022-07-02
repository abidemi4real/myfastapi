from fastapi import FastAPI
from . import models
from .database import  engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) # thic line create table with sqlachelmy after every code runs

app = FastAPI()

origin = ['https://www.google.com','https://www.heroku.com']
#origin = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message" : "Alhamdulillah: It is a success"}



#fetch("http://localhost:8000/").then(res=> res.json()).then(console.log)
