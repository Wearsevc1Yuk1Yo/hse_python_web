import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "Blog API"
    PROJECT_VERSION: str = "1.0.0"
    DATA_FILE: str = os.getenv("BLOG_DATA_FILE", "blog_data.json")
    
settings = Settings()