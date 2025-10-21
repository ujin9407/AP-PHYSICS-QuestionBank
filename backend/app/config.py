from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # DaTikZv2 API Configuration
    datikz_api_key: str = ""
    datikz_api_url: str = "https://api.datikz.com/v2"
    
    # File Upload Configuration
    max_upload_size: int = 10485760  # 10MB
    upload_dir: str = "uploads"
    output_dir: str = "outputs"
    template_dir: str = "templates"
    
    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Create necessary directories
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.output_dir, exist_ok=True)
os.makedirs(settings.template_dir, exist_ok=True)
