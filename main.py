import os

from models import BASE
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
db = create_engine(os.getenv("DATABASE_URL"))
BASE.metadata.create_all(bind=db)

app = FastAPI()

oatuh2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from man_routes import man_router

app.include_router(auth_router)
app.include_router(man_router)

