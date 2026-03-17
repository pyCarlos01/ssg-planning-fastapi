import os

from fastapi import FastAPI
from dotenv import load_dotenv
from models import BASE, engine
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

oatuh2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from man_routes import man_router

app.include_router(auth_router)
app.include_router(man_router)

BASE.metadata.create_all(bind=engine)
