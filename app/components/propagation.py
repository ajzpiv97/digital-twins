import streamlit as st
import pandas as pd

def render_propagation_trace(df_propagated: pd.DataFrame):
    """
    Renders the propagated failure sequence as a trace/timeline using native
    Streamlit components to show how a failure propagates.
    """
    st.subheader("🌋 Failure Propagation Trace")
    
    if df_propagated is None or df_propagated.empty:
        st.info("No failure propagation available.")
        return

    origins = df_propagated["OriginalSensor"].unique()

    if len(origins) > 1:
        selected_origin = st.selectbox("Select Root Cause Signature to Trace", origins)
    else:
        selected_origin = origins[0]
        st.markdown(f"**Root Cause Signature:** `{selected_origin}`")

    # Filter to only the selected origin trace
    df_subset = df_propagated[df_propagated["OriginalSensor"] == selected_origin].sort_values(by="PropagationOrder")
    
    st.divider()

    with st.container(height=500, border=False):
        for idx, row in df_subset.iterrows():
            order = row['PropagationOrder']
            orig = row['OriginalSensor']
            target = row['NextAffected']
            
            # Using the first element as the Origin
            if row.equals(df_subset.iloc[0]):
                icon = "💥"
                title = f"**Origin:** {orig}"
                detail = f"Failure originated here and propagated to `{target}`"
                color = "red"
            else:
                icon = "🔻"
                title = f"**Impact:** {target}"
                detail = "Propagated downstream in severity chain"
                color = "orange"

            # Use columns and markdown to simulate a timeline item without raw HTML
            col_icon, col_text = st.columns([1, 11])
            with col_icon:
                st.subheader(icon)
            with col_text:
                st.markdown(f"**Step {order}** | :{color}[{title}]")
                st.caption(detail)
