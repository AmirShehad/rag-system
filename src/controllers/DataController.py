from .BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale=1048576
    def validate_upladed_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False
        if file.size > self.app_settings.FILE_SIZE_MAX * self.size_scale:
            return False

        return True    