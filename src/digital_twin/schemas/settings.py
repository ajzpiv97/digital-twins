from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from typing import Literal

class Settings(BaseSettings):
    processed_data_dir: Path
    app_env: Literal["local", "platform"] = "local"  # 'local' or 'platform'

    # Prometheux backend (optional — required for data refresh)
    pmtx_token: str = ""
    pmtx_project: str = ""
    concept_centrality: str = "component_centrality"
    concept_shortest_path: str = "shortest_path"
    concept_hotspot: str = "hotspot_metadata"
    concept_linked_to: str = "linked_to"
    concept_propagated_failure: str = "propagated_failure"

    model_config = ConfigDict(
        extra="ignore"
    )

@lru_cache
def get_settings():
    return Settings()
