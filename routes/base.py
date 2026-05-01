from fastapi import FastAPI, APIRouter
import os

base_rotuer=APIRouter(
    prefix='/api/v1',
    tags=['api_v1'],
)

@base_rotuer.get("/")
def welcome():
    app_name=os.getenv('APP_NAME')
    app_version=os.getenv('APP_version')
    return{
        "App_Name" : app_name,
        "App_version": app_version
    }