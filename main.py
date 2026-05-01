from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv('.env')
from routes.base import base_rotuer 

app = FastAPI()
app.include_router(base_rotuer)