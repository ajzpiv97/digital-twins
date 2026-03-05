import streamlit as st
import pandas as pd
from components.graphs import render_topology_graph, render_centrality_table
from components.chat import render_chat_interface
from components.propagation import render_propagation_trace

def render_diagnostics(df_centrality: pd.DataFrame, df_paths: pd.DataFrame, df_hotspots: pd.DataFrame, df_linked_to: pd.DataFrame | None, df_propagated: pd.DataFrame, top_nodes: list):
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.subheader("🕸️ Topology & Failure Paths")
        render_topology_graph(df_paths, df_linked_to)
        
    with col2:
        render_propagation_trace(df_propagated)
        
        st.divider()
        st.subheader("🤔 Why this hotspot?")
        st.info("The root cause analysis engine traced the cascading anomaly signatures back to the originating sensor. The topology graph confirms a direct propagation path through high-centrality components.")
    
    st.divider()

    st.subheader("🚨 Active Alerts")
    if top_nodes:
        st.error(f"**CRITICAL:** High anomaly probability detected across **{len(top_nodes)}** high-centrality node(s). See centrality table below for details.")
    
    with st.expander("View Centrality DataFrame (Vadalog #DC Output)", expanded=True):
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; font-size:0.82rem; color:#aaa;">
              <span>🟥 Darker red = Higher Centrality Score = <strong style="color:#ff4b4b">Greater failure impact risk</strong></span>
              &nbsp;|&nbsp;
              <span style="display:inline-flex; align-items:center; gap:4px;">
                <span style="background:#fff0f0; width:18px; height:12px; display:inline-block; border:1px solid #ccc; border-radius:2px;"></span> Low
                <span style="background:#ff9999; width:18px; height:12px; display:inline-block; border:1px solid #ccc; border-radius:2px;"></span>
                <span style="background:#ff4b4b; width:18px; height:12px; display:inline-block; border-radius:2px;"></span>
                <span style="background:#8b0000; width:18px; height:12px; display:inline-block; border-radius:2px;"></span> High
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        render_centrality_table(df_centrality)

    st.divider()
    with st.expander("💬 Prometheux Assistant", expanded=False):
        render_chat_interface()
