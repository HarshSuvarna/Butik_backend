from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from src.api import (
    otp,
    user,
    store,
    product,
    variant,
    filter,
    attribute,
    bulk_upload,
    transaction,
)
from src.db.database import engine, SessionLocal
import src.db.models as models


load_dotenv()
models.Base.metadata.create_all(engine)

app = FastAPI(
    title="BUTIK APIs",
    description="APIs for veiwing nearby stores and products",
    version="0.0.1",
    contact={
        "name": "Harsh Suvarna",
        "email": "harsh.suvarna9962@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def get_health():
    return {"status": "OK"}


@app.get("/")
def cover():
    return "BUTIK APIS"


app.include_router(otp.router)
app.include_router(user.router)
app.include_router(store.router)
app.include_router(product.router)
app.include_router(variant.router)
app.include_router(filter.router)
app.include_router(attribute.router)
app.include_router(bulk_upload.router)
app.include_router(transaction.router)
