from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    FILE_ALLOWED_TYPE:list
    FILE_SIZE_MAX:int

    model_config = SettingsConfigDict(env_file='.env')

def get_settings():
    return settings()        