from fastapi import FastAPI
from routes.base import base_rotuer 

app = FastAPI()
app.include_router(base_rotuer)