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
settings = get_settings()

# Safe base path — falls back to cwd if PROCESSED_DATA_DIR is not set
try:
    _base = settings.processed_data_dir
except Exception:
    _base = None

def _default(subdir: str) -> str:
    return str(_base / subdir) if _base else ""

with st.sidebar:
    # st.header("⚙️ Configuration")
    # with st.form("folder_config", border=False):
    #     centrality_folder = st.text_input("Centrality Data Folder", value=_default("component_centrality"))
    #     paths_folder = st.text_input("Shortest Paths Folder", value=_default("shortest_path"))
    #     hotspots_folder = st.text_input("Hotspots Metadata Folder", value=_default("hotspot_metadata"))
    #     linked_to_folder = st.text_input("Component Relationships Folder", value=_default("linked_to"))
    #     st.form_submit_button("Apply", use_container_width=True)
    render_refresh_button(settings)

# Load Data
df_centrality = DataLoader.get_centrality_data(_base / settings.concept_centrality)
df_paths = DataLoader.get_shortest_paths(_base / settings.concept_shortest_path)
df_hotspots = DataLoader.get_hotspot_metadata(_base / settings.concept_hotspot)
df_linked_to = DataLoader.get_linked_to(_base / settings.concept_linked_to)
df_propagated = DataLoader.get_propagated_failures(_base / settings.concept_propagated_failure)

# --- State Management for simulated RCA actions ---
if "resolved_components" not in st.session_state:
    st.session_state["resolved_components"] = []
if "resolved_sensors" not in st.session_state:
    st.session_state["resolved_sensors"] = []

resolved_components = st.session_state["resolved_components"]
resolved_sensors = st.session_state["resolved_sensors"]

if resolved_components:
    # Filter the active data matching the resolved list
    if df_hotspots is not None and not df_hotspots.empty:
        df_hotspots = df_hotspots[~df_hotspots["Component"].isin(resolved_components)]
        
    if df_centrality is not None and not df_centrality.empty:
        df_centrality = df_centrality[~df_centrality["Component"].isin(resolved_components)]
        
    if df_paths is not None and not df_paths.empty:
        # Remove paths touching resolved nodes
        df_paths = df_paths[~(df_paths["StartNode"].isin(resolved_components) | df_paths["EndNode"].isin(resolved_components))]
        
    if df_linked_to is not None and not df_linked_to.empty:
        df_linked_to = df_linked_to[~(df_linked_to["Parent"].isin(resolved_components) | df_linked_to["Component"].isin(resolved_components))]

if resolved_sensors:
    if df_propagated is not None and not df_propagated.empty:
        df_propagated = df_propagated[~df_propagated["OriginalSensor"].isin(resolved_sensors)]

# --- Computations for top-level KPIs ---
total_components = len(df_centrality)
critical_count = df_hotspots['Component'].nunique() if df_hotspots is not None and not df_hotspots.empty else 0

if not df_centrality.empty:
    max_score = df_centrality['CentralityScore'].max()
    top_nodes = df_centrality[df_centrality['CentralityScore'] == max_score]['Component'].tolist()
else:
    top_nodes = []

# --- Header ---
st.title("🚀 Digital Twin Demo: Rocket Engine Failure Detection & Response")
st.markdown("Revolutionizing Aerospace Safety Through Intelligent Failure Prediction and Response")

# --- Top-Level KPIs ---
st.subheader("System Overview")
metric1, metric2, metric3 = st.columns(3)
metric1.metric("Monitored Components", str(total_components))
hotspot_delta = "⚠ Requires Attention" if critical_count > 0 else "✓ All Clear"
hotspot_delta_color = "inverse" if critical_count > 0 else "normal"
metric2.metric("Critical Hotspots", str(critical_count), hotspot_delta, delta_color=hotspot_delta_color)
metric3.metric("High Centrality Nodes", str(len(top_nodes)), "High Risk", delta_color="inverse")
st.divider()

# --- Tabs ---
# As per feedback, we simplify the tabs to focus strongly on the action-oriented flow
tab1, tab2 = st.tabs(["**Live Diagnostics & Tracing**", "**Root Cause Actions & Notifications**"])

with tab1:
    render_diagnostics(df_centrality, df_paths, df_hotspots, df_linked_to, df_propagated, top_nodes)

with tab2:
    render_root_cause_analysis(df_hotspots)