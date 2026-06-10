from fastapi import FastAPI, APIRouter, Depends, UploadFile, File, status, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignal
import aiofiles
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk

logger=logging.getLogger('uvicorn.error')

data_controller=DataController()
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request,project_id : str,file: UploadFile=File(...),
                      app_settings: settings=Depends(get_settings)):
    
    project_model=ProjectModel(
        db_client= request.app.db_client
        )
    project= await project_model.get_project_or_create_one(project_id=project_id)    

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
            "file_id" : file_id,
        } 
    )

@data_router.post("/process/{project_id}")
async def prcoess_endpoint(request: Request,project_id:str, process_request: ProcessRequest):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    do_reset=process_request.do_reset

    project_model=ProjectModel(db_client= request.app.db_client)
    project= await project_model.get_project_or_create_one(project_id=project_id)



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

    file_chunk_records=[
        DataChunk(
            chunk_text= chunk.page_content,
            chunk_metadata= chunk.metadata, 
            chunk_order= i+1, 
            chunk_project_id= str(project.id),
        )
        for i, chunk in enumerate(file_chunk)
    ]
    
    chunk_model=ChunkModel(db_client=request.app.db_client)
    if do_reset== 1:
        _ =await chunk_model.delete_chunk_by_project_id(project_id= project.id)

    no_records=await chunk_model.insert_many_chunks(chunks=file_chunk_records)
    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )