import streamlit as st
from digital_twin.data_loader import load_centrality_data, load_shortest_paths
from digital_twin.components.graphs import render_topology_graph
from digital_twin.components.chat import render_chat_interface

# --- Page Config ---
st.set_page_config(
    page_title="Prometheux Engine Twin", 
    page_icon="🚀", 
    layout="wide"
)

# --- Header ---
st.title("🚀 Engine Digital Twin Diagnostics")
st.markdown("Real-time topology and failure propagation analysis powered by **Prometheux Vadalog**.")

# Load Data
df_centrality = load_centrality_data()
df_paths = load_shortest_paths()

# Extract key metrics
highest_risk = df_centrality.iloc[0]['Component'] if not df_centrality.empty else "N/A"
total_components = len(df_centrality)

# --- Layout Grid ---
col_main, col_chat = st.columns([7, 3], gap="large")

with col_main:
    # 1. Top Level Metrics
    st.subheader("System Overview")
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Monitored Components", str(total_components), "+2 Active")
    metric2.metric("Critical Hotspots", "1", "-1 Resolved")
    metric3.metric("Highest Centrality Node", highest_risk, "High Risk", delta_color="inverse")
    
    st.divider()
    
    # 2. Interactive Network Graph
    render_topology_graph(df_paths)
    
    st.divider()

    # 3. Live Sensor Alerts (Simulated)
    st.subheader("🚨 Active Alerts")
    
    # Create an alert card that points to the most central component
    st.error(f"**CRITICAL:** High anomaly probability detected on downstream path from {highest_risk}.")
    
    with st.expander("View Centrality DataFrame (Vadalog #DC Output)", expanded=True):
        st.dataframe(
            df_centrality.style.background_gradient(cmap='Reds', subset=['CentralityScore']), 
            use_container_width=True
        )

with col_chat:
    # 4. Prometheux Chat Interface
    render_chat_interface()