import streamlit as st
from digital_twin.data_loader import DataLoader
from digital_twin.schemas.settings import get_settings
from views.overview import render_overview
from views.live_diagnostics import render_diagnostics
from views.root_cause_analysis import render_root_cause_analysis
from components.refresh import render_refresh_button

# --- Page Config ---
st.set_page_config(
    page_title="Prometheux Engine Twin", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    settings = get_settings()
    # Let the user provide the folder locations
    centrality_folder = st.text_input("Centrality Data Folder", value=str(settings.processed_data_dir / "component_centrality"))
    paths_folder = st.text_input("Shortest Paths Folder", value=str(settings.processed_data_dir / "shortest_path"))
    hotspots_folder = st.text_input("Hotspots Metadata Folder", value=str(settings.processed_data_dir / "hotspot_metadata"))
    linked_to_folder = st.text_input("Component Relationships Folder", value=str(settings.processed_data_dir / "linked_to"))
    render_refresh_button(settings)

# Load Data
df_centrality = DataLoader.get_centrality_data(centrality_folder)
df_paths = DataLoader.get_shortest_paths(paths_folder)
df_hotspots = DataLoader.get_hotspot_metadata(hotspots_folder)
df_linked_to = DataLoader.get_linked_to(linked_to_folder)

# --- Header ---
st.title("🚀 Digital Twin Demo: Rocket Engine Failure Detection & Response")
st.markdown("Revolutionizing Aerospace Safety Through Intelligent Failure Prediction and Response")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["**Overview**", "**Live Diagnostics**", "**Root Cause Analysis**"])

with tab1:
    render_overview()

with tab2:
    render_diagnostics(df_centrality, df_paths, df_hotspots, df_linked_to)

with tab3:
    render_root_cause_analysis(df_hotspots)