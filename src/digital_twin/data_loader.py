import pandas as pd
from pathlib import Path
import streamlit as st
from dataclasses import dataclass

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
        if folder.exists() and folder.is_dir():
            parquet_files = list(folder.glob("*.parquet"))
            if parquet_files:
                return pd.read_parquet(parquet_files[0])
        return None

    @classmethod
    def get_centrality_data(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves Degree Centrality (#DC) output."""
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            return df
        
        # Fallback mock data for presentation safety
        return pd.DataFrame({
            "Component": ["HPOTP", "Main_Valve", "Fuel_Pump", "Nozzle", "Sensor_A"],
            "CentralityScore": [0.85, 0.62, 0.41, 0.30, 0.15]
        })

    @classmethod
    def get_shortest_paths(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves All-Pairs Shortest Path (#ASP) output."""
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            return df
        
        # Fallback mock data mapping connections
        return pd.DataFrame({
            "StartNode": ["Sensor_A", "Sensor_A", "Fuel_Pump", "Main_Valve"],
            "EndNode": ["Fuel_Pump", "HPOTP", "HPOTP", "Nozzle"],
            "Dist": [1, 2, 1, 1]
        })

    @classmethod
    def get_hotspot_metadata(cls, folder_path: str | Path) -> pd.DataFrame:
        """Retrieves Hotspot Metadata output."""
        df = cls.load_parquet_from_folder(str(folder_path))
        if df is not None:
            if "CausesList" in df.columns:
                df["CausesList"] = df["CausesList"].apply(
                    lambda causes: [CauseMetadata(**c) for c in causes] if isinstance(causes, list) else causes
                )
            return df
        
        # Fallback mock data for presentation safety
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