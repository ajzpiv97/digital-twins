from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path

class Settings(BaseSettings):
    processed_data_dir: Path
    model_config = ConfigDict(
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()
