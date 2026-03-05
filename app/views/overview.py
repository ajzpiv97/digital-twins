import streamlit as st

def render_overview():
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
