from fastapi import FastAPI
from routes import user
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI() 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"], 
    allow_headers=["*"],
)


app.include_router(user)


@app.get("/")
def cover_page():
    return "Butik APIs"
