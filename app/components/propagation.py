import streamlit as st
import pandas as pd

def render_propagation_trace(df_propagated: pd.DataFrame):
    """
    Renders the propagated failure sequence as a trace/timeline to show
    how a failure propagates through the system components.
    """
    st.subheader("🌋 Failure Propagation Trace")
    
    if df_propagated is None or df_propagated.empty:
        st.info("No failure propagation available.")
        return

    st.markdown('''
    <style>
    .timeline-container {
        border-left: 2px solid #FF4B4B;
        margin-left: 15px;
        padding-left: 20px;
    }
    .timeline-item {
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: "";
        position: absolute;
        width: 12px;
        height: 12px;
        background: #FF4B4B;
        border-radius: 50%;
        left: -27px;
        top: 5px;
    }
    .timeline-title {
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 5px;
        font-size: 1.1em;
    }
    .timeline-detail {
        color: #a0a0a0;
        font-size: 0.9em;
    }
    .timeline-original {
        color: #FF4B4B;
        font-weight: bold;
    }
    </style>
    ''', unsafe_allow_html=True)

    origins = df_propagated["OriginalSensor"].unique()

    if len(origins) > 1:
        selected_origin = st.selectbox("Select Root Cause Signature to Trace", origins)
    else:
        selected_origin = origins[0]
        st.markdown(f"**Root Cause Signature:** `{selected_origin}`")

    # Filter to only the selected origin trace
    df_subset = df_propagated[df_propagated["OriginalSensor"] == selected_origin].sort_values(by="PropagationOrder")
    
    # We can wrap the timeline in a scrollable container to save space
    # if it gets too long.
    with st.container(height=500, border=False):
        html_content = '<div class="timeline-container">'
        
        for idx, row in df_subset.iterrows():
            order = row['PropagationOrder']
            orig = row['OriginalSensor']
            target = row['NextAffected']
            
            # Using the first element as the Origin
            if row.equals(df_subset.iloc[0]):
                title = f"💥 Origin: {orig}"
                detail = f"Failure originated here and propagated to {target}"
            else:
                title = f"🔻 Impact: {target}"
                detail = f"Propagated downstream in severity chain"
                
            html_content += f'''
            <div class="timeline-item">
                <div class="timeline-title">{title}</div>
                <div class="timeline-detail">{detail}</div>
                <div class="timeline-detail" style="font-size: 0.8em; margin-top:2px;">Sequence Step: {order}</div>
            </div>
            '''
            
        html_content += '</div>'
        
        st.markdown(html_content, unsafe_allow_html=True)
