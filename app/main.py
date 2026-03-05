import streamlit as st
from digital_twin.data_loader import DataLoader
from components.graphs import render_topology_graph
from components.chat import render_chat_interface
from digital_twin.schemas.settings import get_settings
from pathlib import Path

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

# Load Data
df_centrality = DataLoader.get_centrality_data(centrality_folder)
df_paths = DataLoader.get_shortest_paths(paths_folder)
df_hotspots = DataLoader.get_hotspot_metadata(hotspots_folder)

# --- Header ---
st.title("🚀 Digital Twin Demo: Rocket Engine Failure Detection & Response")
st.markdown("Revolutionizing Aerospace Safety Through Intelligent Failure Prediction and Response")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["**Overview**", "**Live Diagnostics**", "**Root Cause Analysis**"])

with tab1:
    st.markdown("""
    ## 🔬 What is a Digital Twin?
    A Digital Twin is a sophisticated virtual replica of a physical system that mirrors its real-world counterpart in real-time. Think of it as a **"living simulation"** that continuously learns from and responds to actual operational data, enabling unprecedented levels of monitoring, analysis, and predictive capabilities.
    """)
    
    st.info("""
    **🔄 Core Concept**
    
    `Physical System ←→ Digital Twin`
    
    Sensors ↕ ↕ Continuous Analysis & Prediction
    """)

    col_char, col_aero = st.columns(2)
    with col_char:
        st.markdown("""
        ### 🎯 Key Characteristics
        This digital twin demo is characterized by several powerful capabilities that bring both analytical depth and operational value:
        - **Real-time synchronization** with sensor data, ensuring instant awareness of the system’s condition.
        - **Logical reasoning** to discover failures in advance, supporting proactive maintenance rather than reactive response.
        - **Simulate what-if scenarios** enabling engineers to test modifications and conditions in a virtual environment without real-world risk.
        - **Root cause analysis** automatically tracing complex failures to their origins through recursive reasoning.
        - **Robust decision support** empowering teams with data-driven insights that lead to faster and more informed operational actions.
        """)

    with col_aero:
        st.markdown("""
        ### 🎯 Aerospace Application
        Digital Twins are revolutionizing aerospace operations by addressing critical industry challenges:
        
        **🔧 Failure Prevention**: *"Prevent failures before they occur"*
        Instead of reactive maintenance, Digital Twins analyze sensors pattern to prevent component degradation, enabling proactive scheduling, extended lifespans, and reduced unplanned downtime.
        
        **📊 Real-Time Health Monitoring**: *"Every sensor tells a story"*
        Continuous analysis of temperature, pressure, vibration, performance metrics, and component interactions.
        
        **🔍 Rapid Root Cause Analysis**: *"Trace the invisible connections"*
        When anomalies occur, instantly map complex component relationships, identify hidden failure chains, pinpoint true root causes, and suggest optimal resolution paths.
        
        **⚡ Operational Optimization**: *"Simulate before you operate"*
        Virtual testing enables performance optimization under various conditions, safety margin validation, and risk mitigation.
        """)
        
    st.divider()
    
    st.subheader("🚀 Rocket Engines Need Digital Twins")
    st.markdown("""
    **Mission Context**
    Space missions demand unprecedented reliability and safety standards. Failures in rocket engines can result in catastrophic mission outcomes, loss of human life, billions in financial damage, and irreparable reputation damage.

    **Demo Focus: Space Shuttle Main Engine (SSME)**
    This Digital Twin demonstration showcases Prometheux's capabilities in automating:
    - **Failure Detection**: Instant identification of component issues
    - **Root Cause Diagnosis**: Precise tracing of failure chains
    - **Automated Response**: Immediate safety and operational actions
    - **Team Coordination**: Intelligent alert routing to responsible personnel
    """)


with tab2:
    highest_risk = df_centrality.iloc[0]['Component'] if not df_centrality.empty else "N/A"
    total_components = len(df_centrality)

    col_main, col_chat = st.columns([7, 3], gap="large")

    with col_main:
        st.subheader("System Overview")
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Monitored Components", str(total_components), "+2 Active")
        metric2.metric("Critical Hotspots", "1", "-1 Resolved")
        metric3.metric("Highest Centrality Node", highest_risk, "High Risk", delta_color="inverse")
        
        st.divider()
        
        render_topology_graph(df_paths)
        
        st.divider()

        st.subheader("🚨 Active Alerts")
        st.error(f"**CRITICAL:** High anomaly probability detected on downstream path from {highest_risk}.")
        
        with st.expander("View Centrality DataFrame (Vadalog #DC Output)", expanded=True):
            st.dataframe(
                df_centrality.style.background_gradient(cmap='Reds', subset=['CentralityScore']), 
                width='stretch'
            )

    with col_chat:
        render_chat_interface()


with tab3:
    st.header("🔍 Root Cause Analysis & Personnel Routing")
    st.markdown("Immediate safety and operational actions automatically traced to responsible engineering teams.")
    
    if df_hotspots is not None and not df_hotspots.empty:
        for idx, row in df_hotspots.iterrows():
            with st.container(border=True):
                st.subheader(f"🛠️ {row['Component']} Degradation Alert")
                subcol1, subcol2 = st.columns([1, 2])
                
                with subcol1:
                    st.info(f"""
                    **Assigned Response Team:**
                    - **Team:** {row['Team']}
                    - **Lead:** {row['FullName']}
                    """)
                    
                with subcol2:
                    st.markdown("**🚨 Underlying Sensor Triggers (Root Causes):**")
                    causes = row['CausesList']
                    
                    for c in causes:
                        st.error(f"**{c['sensor']}** — Code: `{c['code']}` | Related: `{c['related']}`", icon="⚠️")
                
                st.divider()
                if st.button(f"✉️ Page {row['FullName']} & Send Diagnostic Report", key=f"email_{idx}"):
                    st.toast(f"Critical report successfully routed to {row['FullName']}!", icon="✅")
                    st.success(f"Diagnostics payload transmitted to the **{row['Team']}** operations channel.")
    else:
        st.info("No active hotspots currently demanding attention.")