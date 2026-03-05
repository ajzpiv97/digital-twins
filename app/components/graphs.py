import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
import logging

try:
    from digital_twin.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    logger = logging.getLogger(__name__)

@st.cache_data(show_spinner=False)
def _build_graph_html(df_paths: pd.DataFrame) -> str:
    """
    Builds the PyVis network HTML from edge data.
    Cached by Streamlit — only rebuilds when df_paths changes.
    """
    logger.info("Building topology graph — %d edges", len(df_paths))
    net = Network(height="400px", width="100%", bgcolor="#0E1117", font_color="white")

    for _, row in df_paths.iterrows():
        src = str(row['StartNode'])
        dst = str(row['EndNode'])
        weight = row['Dist']
        net.add_node(src, label=src, color="#FF4B4B")
        net.add_node(dst, label=dst, color="#FF4B4B")
        net.add_edge(src, dst, title=f"Distance: {weight}")

    net.repulsion(node_distance=100, spring_length=200)

    path = "/tmp/pyvis_graph.html"
    net.save_graph(path)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    logger.debug("Graph HTML built (%d chars)", len(html))
    return html


def _build_centrality_style(df: pd.DataFrame):
    """
    Applies background_gradient styling to the centrality DataFrame.
    NOTE: Styler objects cannot be pickled, so this is NOT cached.
    """
    logger.debug("Building centrality gradient style")
    return df.style.background_gradient(cmap='Reds', subset=['CentralityScore'])


def render_topology_graph(df_paths: pd.DataFrame, df_linked_to: pd.DataFrame | None = None):
    """Renders the interactive PyVis graph (cached) and optional parent→child table."""
    try:
        html_data = _build_graph_html(df_paths)
        components.html(html_data, height=410)
    except Exception as e:
        logger.error("Graph rendering failed: %s", e)
        st.error(f"Graph rendering failed: {e}")

    # --- Collapsible Component Relationship Table ---
    if df_linked_to is not None and not df_linked_to.empty:
        with st.expander("🔗 View Component Relationships (Parent → Child)", expanded=False):
            st.caption("Each row shows a direct dependency: the Parent component propagates failures downstream to its linked Component.")
            grouped = df_linked_to.groupby("Parent")["Component"].apply(list).reset_index()
            grouped.columns = ["Parent", "Linked Components"]
            grouped["Linked Components"] = grouped["Linked Components"].apply(lambda cs: " → ".join(cs))
            st.dataframe(grouped, width='stretch', hide_index=True)


def render_centrality_table(df: pd.DataFrame):
    """Renders the centrality DataFrame with a cached background gradient style."""
    styled = _build_centrality_style(df)
    st.dataframe(styled, width='stretch')