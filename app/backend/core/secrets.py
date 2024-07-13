import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_app_name():
    return os.getenv("APP_NAME")


def get_debug_mode():
    return os.getenv("DEBUG_MODE")


def get_knowledge_base_dir():
    return os.getenv("KNOWLEDGE_BASE_DIR")


def get_google_api_key():
    return os.getenv("GOOGLE_API_KEY")


def get_google_api_key():
    return os.getenv("GOOGLE_API_KEY")


def get_google_api_key():
    return os.getenv("GOOGLE_API_KEY")

def get_openai_key():
    return os.getenv("OPENAI_API_KEY")

def get_ngrok_token():
    return os.getenv("NGROK_AUTHTOKEN")

def get_aws_key_id():
    return os.getenv("AWS_ACCESS_KEY_ID")

def get_aws_secret_access_key():
    return os.getenv("AWS_SECRET_ACCESS_KEY")

def get_aws_region():
    return os.getenv("AWS_REGION")