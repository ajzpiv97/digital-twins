import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd

def render_topology_graph(df_paths: pd.DataFrame):
    """Generates an interactive HTML network graph from edge data."""
    st.subheader("🕸️ Topology & Failure Paths")
    
    # Initialize PyVis network
    net = Network(height="400px", width="100%", bgcolor="#0E1117", font_color="white")
    
    # Add nodes and edges from our Shortest Path dataset
    for _, row in df_paths.iterrows():
        src = str(row['StartNode'])
        dst = str(row['EndNode'])
        weight = row['MinHops']
        
        net.add_node(src, label=src, color="#FF4B4B")
        net.add_node(dst, label=dst, color="#FF4B4B")
        net.add_edge(src, dst, title=f"Hops: {weight}")
        
    # Configure physics for a cool interactive bounce effect
    net.repulsion(node_distance=100, spring_length=200)
    
    # Save to a temporary HTML file and render it in Streamlit
    try:
        path = "/tmp/pyvis_graph.html"
        net.save_graph(path)
        with open(path, "r", encoding="utf-8") as f:
            html_data = f.read()
        components.html(html_data, height=410)
    except Exception as e:
        st.error(f"Graph rendering failed: {e}")