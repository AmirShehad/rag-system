from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, settings
base_rotuer=APIRouter(
    prefix='/api/v1',
    tags=['api_v1'],
)

@base_rotuer.get("/")
async def welcome(app_settings : settings =Depends(get_settings)):
    
    app_name=app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    return{
        "App_Name" : app_name,
        "App_version": app_version
    }