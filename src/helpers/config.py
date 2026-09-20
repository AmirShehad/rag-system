from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str

    FILE_ALLOWED_TYPE:list
    FILE_SIZE_MAX:int
    FILE_CHUNK_SIZE:int

    MONGODB_URL:str
    MONGODB_DATABASE:str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str=None
    OPENAI_API_URL: str=None
    COHERE_API_KEY: str=None

    GENERATION_MODEL_ID: str=None
    EMBEDDING_MODEL_ID: str=None
    EMBEDDING_MODEL_SIZE: int=None
    INPUT_DEFAULT_MAX_CHARACTERS: int=None
    GENERATION_DEFAULT_MAX_TOKENS: int=None
    GENERATION_DEFAULT_TEMPERATURE: float=None


    model_config = SettingsConfigDict(env_file='.env')

def get_settings():
    return settings()        