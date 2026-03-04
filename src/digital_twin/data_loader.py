import pandas as pd
from pathlib import Path
import streamlit as st

# Point this to where your JupyterLab Part 1 outputs are stored
DATA_DIR = Path(__file__).parent.parent.parent / "data"

@st.cache_data
def load_centrality_data() -> pd.DataFrame:
    """Loads Degree Centrality (#DC) output."""
    file_path = DATA_DIR / "degree_centrality.parquet"
    if file_path.exists():
        return pd.read_parquet(file_path)
    
    # Fallback mock data for presentation safety
    return pd.DataFrame({
        "Component": ["HPOTP", "Main_Valve", "Fuel_Pump", "Nozzle", "Sensor_A"],
        "CentralityScore": [0.85, 0.62, 0.41, 0.30, 0.15]
    })

@st.cache_data
def load_shortest_paths() -> pd.DataFrame:
    """Loads All-Pairs Shortest Path (#ASP) output."""
    file_path = DATA_DIR / "shortest_path.parquet"
    if file_path.exists():
        return pd.read_parquet(file_path)
    
    # Fallback mock data mapping connections
    return pd.DataFrame({
        "StartNode": ["Sensor_A", "Sensor_A", "Fuel_Pump", "Main_Valve"],
        "EndNode": ["Fuel_Pump", "HPOTP", "HPOTP", "Nozzle"],
        "MinHops": [1, 2, 1, 1]
    })