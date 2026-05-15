from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id : str,file: UploadFile=File(...),
                      app_settings: settings=Depends(get_settings)):
    

    is_valid, response_signal=DataController().validate_upladed_file(file=file)
    #if is_valid:
    #    return {
    #   "is_valid": is_valid,
    #   "response_signal": response_signal.value
    #   }
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message" : response_signal.value
            }
        )
    project_dir_path=ProjectController().project_path(project_id=project_id)
    file_path=os.path.join(
        project_dir_path,file.filename
    )
    async with aiofiles.open(file_path,"wb") as f:
        while chunk:= await file.read(app_settings.FILE_CHUNK_SIZE):
            await f.write(chunk)

    return JSONResponse(
        content={
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value
        } 
    )        