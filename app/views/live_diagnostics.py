import streamlit as st
import pandas as pd
from components.graphs import render_topology_graph
from components.chat import render_chat_interface

def render_diagnostics(df_centrality: pd.DataFrame, df_paths: pd.DataFrame, df_hotspots: pd.DataFrame, df_linked_to: pd.DataFrame | None = None):
    # --- Compute Metrics from real data ---
    total_components = len(df_centrality)

    if not df_centrality.empty:
        max_score = df_centrality['CentralityScore'].max()
        top_nodes = df_centrality[df_centrality['CentralityScore'] == max_score]['Component'].tolist()
    else:
        top_nodes = []

    # Critical hotspots = unique affected components in hotspot metadata
    critical_count = df_hotspots['Component'].nunique() if df_hotspots is not None and not df_hotspots.empty else 0

    col_main, col_chat = st.columns([7, 3], gap="large")

    with col_main:
        st.subheader("System Overview")
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Monitored Components", str(total_components))
        hotspot_delta = "⚠ Requires Attention" if critical_count > 0 else "✓ All Clear"
        hotspot_delta_color = "inverse" if critical_count > 0 else "normal"
        metric2.metric("Critical Hotspots", str(critical_count), hotspot_delta, delta_color=hotspot_delta_color)
        metric3.metric("High Centrality Nodes", str(len(top_nodes)), "High Risk", delta_color="inverse")
        
        st.divider()
        
        render_topology_graph(df_paths, df_linked_to)
        
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
            st.dataframe(
                df_centrality.style.background_gradient(cmap='Reds', subset=['CentralityScore']), 
                width='stretch'
            )

    with col_chat:
        render_chat_interface()
