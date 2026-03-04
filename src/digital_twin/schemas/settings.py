from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    processed_data_dir: str
    model_config = ConfigDict(
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()
