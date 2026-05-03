from fastapi import FastAPI, APIRouter, Depends, UploadFile, File
import os
from helpers.config import get_settings, settings
from controllers import DataController
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=['api_v1','data']
)

@data_router.post('/upload/{project_id}')
async def upload_data(project_id : str,file: UploadFile=File(...),
                      app_settings: settings=Depends(get_settings)):
    

    is_valid=DataController().validate_upladed_file(file=file)

    return is_valid