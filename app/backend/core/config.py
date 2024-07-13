from pydantic import BaseSettings

from app.backend.core.secrets import (get_app_name, get_aws_key_id,
                                      get_aws_region,
                                      get_aws_secret_access_key,
                                      get_debug_mode, get_google_api_key,
                                      get_knowledge_base_dir, get_ngrok_token,
                                      get_openai_key)


class Settings(BaseSettings):
    APP_NAME: str = "AI Crew API"
    DEBUG_MODE: bool = False
    API_V1_STR: str = "/api/v1"
    KNOWLEDGE_BASE_DIR: str = "data/"

    GOOGLE_API_KEY: str
    OPENAI_API_KEY: str
    NGROK_AUTHTOKEN: str 

    AWS_ACCESS_KEY_ID: str 
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str    

    class Config:
        env_file = ".env"

settings = Settings(
    APP_NAME=get_app_name(),
    DEBUG_MODE=get_debug_mode,
    KNOWLEDGE_BASE_DIR=get_knowledge_base_dir(),
    GOOGLE_API_KEY=get_google_api_key(),
    OPEN_API_KEY=get_openai_key(),
    NGROK_AUTHTOKEN=get_ngrok_token(),
    AWS_ACCESS_KEY_ID=get_aws_key_id(),
    AWS_SECRET_ACCESS_KEY=get_aws_secret_access_key(),
    AWS_REGION=get_aws_region(),
)