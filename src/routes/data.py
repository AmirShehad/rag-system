from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal
import aiofiles
import logging
from .schemes.data import ProcessRequest

logger=logging.getLogger('uvicorn.error')

data_controller=DataController()
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id : str,file: UploadFile=File(...),
                      app_settings: settings=Depends(get_settings)):
    

    is_valid, response_signal=data_controller.validate_uploaded_file(file=file)
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
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    
    #file_path=os.path.join(
    #    project_dir_path,file.filename)
    
    file_path, file_id=data_controller.generate_unique_filepath(
        orign_filename=file.filename,
        project_id=project_id
    )
    try:   
        async with aiofiles.open(file_path,"wb") as f:
            while chunk:= await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file:{e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message" : responseSignal.File_UPLOAD_FAILED.value
            }
        )
    return JSONResponse(
        content={
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id" : file_id
        } 
    )

@data_router.post("/process/{project_id}")
async def prcoess_endpoint(project_id:str, process_request: ProcessRequest):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size

    processcontroller=ProcessController(project_id=project_id)
    file_content=processcontroller.get_file_content(file_id=file_id)

    file_chunk=processcontroller.process_file_content(
        file_id=file_id,
        file_content=file_content,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunk is None or len(file_chunk)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value}
        )

    return file_chunk    