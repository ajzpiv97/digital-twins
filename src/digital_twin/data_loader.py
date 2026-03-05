import pandas as pd
from pathlib import Path
import streamlit as st
from dataclasses import dataclass
from digital_twin.logger import get_logger

logger = get_logger(__name__)

@dataclass
class CauseMetadata:
    sensor: str
    code: str
    related: str

class DataLoader:
    """Handles data extraction and loading for the Digital Twin application."""

    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_parquet_from_folder(folder_path: str) -> pd.DataFrame | None:
        """
        Generalized method to load the first parquet file found in a directory.
        Cached by Streamlit to prevent unnecessary disk reads.
        """
        folder = Path(folder_path)
        logger.debug("Loading parquet from: %s", folder_path)

        if not folder.exists():
            logger.warning("Folder does not exist: %s", folder_path)
            return None
        if not folder.is_dir():
            logger.warning("Path is not a directory: %s", folder_path)
            return None

        parquet_files = list(folder.glob("*.parquet"))
        if not parquet_files:
            logger.warning("No parquet files found in: %s", folder_path)
            return None

        target = parquet_files[0]
        logger.info("Reading parquet file: %s", target.name)
        df = pd.read_parquet(target)
        logger.info("Loaded %d rows, %d columns from %s", len(df), len(df.columns), target.name)
        return df

    @classmethod
    def get_centrality_data(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves Degree Centrality (#DC) output."""
        logger.debug("get_centrality_data — folder: %s", folder_path)
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            return df

        logger.warning("Centrality data not found — using fallback mock data")
        return pd.DataFrame({
            "Component": ["HPOTP", "Main_Valve", "Fuel_Pump", "Nozzle", "Sensor_A"],
            "CentralityScore": [0.85, 0.62, 0.41, 0.30, 0.15]
        })

    @classmethod
    def get_shortest_paths(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves All-Pairs Shortest Path (#ASP) output."""
        logger.debug("get_shortest_paths — folder: %s", folder_path)
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            return df

        logger.warning("Shortest paths data not found — using fallback mock data")
        return pd.DataFrame({
            "StartNode": ["Sensor_A", "Sensor_A", "Fuel_Pump", "Main_Valve"],
            "EndNode": ["Fuel_Pump", "HPOTP", "HPOTP", "Nozzle"],
            "Dist": [1, 2, 1, 1]
        })

    @classmethod
    def get_hotspot_metadata(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves Hotspot Metadata output."""
        logger.debug("get_hotspot_metadata — folder: %s", folder_path)
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            if "CausesList" in df.columns:
                logger.debug("Deserializing CausesList column")
                df["CausesList"] = df["CausesList"].apply(
                    lambda causes: [CauseMetadata(**c) for c in causes] if isinstance(causes, list) else causes
                )
            return df

        logger.warning("Hotspot metadata not found — using fallback mock data")
        return pd.DataFrame({
            "EmpId": ["E001", "E002", "E003", "E004"],
            "FullName": ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince"],
            "Team": ["Maintenance", "Engineering", "Operations", "Safety"],
            "Component": ["HPOTP", "Main_Valve", "Fuel_Pump", "Nozzle"],
            "CausesList": [
                [CauseMetadata(sensor="TEMP_SENSOR_C", code="TC1", related="OVRHT"),
                 CauseMetadata(sensor="TEMP_SENSOR_A", code="TA1", related="OVRHT"),
                 CauseMetadata(sensor="TEMP_SENSOR_B", code="TB1", related="OVRHT")],
                [CauseMetadata(sensor="PRESSURE_VALVE_A", code="PV1", related="PRESS")],
                [CauseMetadata(sensor="VIBRO_SENSOR_1", code="VS1", related="VIB")],
                [CauseMetadata(sensor="THERMAL_RELAY", code="TR1", related="OVRHT")]
            ]
        })

    @classmethod
    def get_linked_to(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves Parent → Component relationship data."""
        logger.debug("get_linked_to — folder: %s", folder_path)
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            return df

        logger.warning("Linked-to data not found — using fallback mock data")
        return pd.DataFrame({
            "Parent": ["HPOTP", "HPOTP", "Main_Valve", "Fuel_Pump"],
            "Component": ["Fuel_Pump", "Sensor_A", "Nozzle", "Sensor_A"],
        })

    @classmethod
    def get_propagated_failures(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves Propagated Failure sequence data."""
        logger.debug("get_propagated_failures — folder: %s", folder_path)
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            return df

        logger.warning("Propagated failure data not found — using fallback mock data")
        return pd.DataFrame({
            "OriginalSensor": ["Sensor_A", "Sensor_A", "Sensor_A"],
            "NextAffected": ["Fuel_Pump", "HPOTP", "Main_Valve"],
            "PropagationOrder": [1, 2, 3]
        })