from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os
class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale=1048576
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED
        if file.size > self.app_settings.FILE_SIZE_MAX * self.size_scale:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED

        return True, ResponseSignal.FILE_UPLOAD_SUCCESS
    def generate_unique_filepath(self, orign_filename:str,project_id:str):
        random_key=self.generate_random_string()
        project_path=ProjectController().get_project_path(project_id=project_id)
        cleaned_name=self.get_clean_filename(orign_filename)
        new_path=os.path.join(project_path, random_key+"_"+cleaned_name)
        
        while os.path.exists(new_path):
            random_key=self.generate_random_string()
            new_path=os.path.join(project_path, random_key+"_"+cleaned_name)
        return new_path, random_key+"_"+cleaned_name  

    def get_clean_filename(self,orgin_filename:str):
        cleaned = re.sub(r'[^\w.]', '', orgin_filename.strip())
        return cleaned.replace(" ","_")