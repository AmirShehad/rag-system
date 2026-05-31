from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader 
from models import ProcessingEnum

class ProcessController(BaseController):
    def __init__(self, project_id:str):
        self.super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id:str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id:str):
        file_ext=get_file_extension(file_id=file_id)
        file_path=os.path.join(self.project_path,file_id)
        if file_ext==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        if file_ext==ProcessingEnum.TXT.value:
            return TextLoader(file_path)    
        return None
    def get_file_content(self, file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        return loader.load()