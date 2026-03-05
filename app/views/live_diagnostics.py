import streamlit as st
from digital_twin.data_loader import DataLoader
from components.graphs import render_topology_graph
from components.chat import render_chat_interface

def render_diagnostics(df_centrality, df_paths):
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
