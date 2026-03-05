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
    
    # Sort just in case it isn't strictly sorted yet
    df_sorted = df_propagated.sort_values(by="PropagationOrder")
    
    html_content = '<div class="timeline-container">'
    
    for _, row in df_sorted.iterrows():
        order = row['PropagationOrder']
        orig = row['OriginalSensor']
        target = row['NextAffected']
        
        # Highlight the first item as the Origin
        if order == 1:
            title = f"💥 Origin: {orig}"
            detail = f"Failure originated here and propagated to {target}"
        else:
            title = f"🔻 Impact: {target}"
            detail = f"Propagated downstream from previous failure points (Root: {orig})"
            
        html_content += f'''
        <div class="timeline-item">
            <div class="timeline-title">{title}</div>
            <div class="timeline-detail">{detail}</div>
            <div class="timeline-detail" style="font-size: 0.8em; margin-top:2px;">Sequence Step: {order}</div>
        </div>
        '''
        
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)
