import streamlit as st
import logging

try:
    from digital_twin.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    logger = logging.getLogger(__name__)

def render_root_cause_analysis(df_hotspots):
    st.header("🔍 Root Cause Analysis & Personnel Routing")
    st.markdown("Immediate safety and operational actions automatically traced to responsible engineering teams.")

    if df_hotspots is None or df_hotspots.empty:
        st.info("No active hotspots currently demanding attention.")
        return

    for idx, row in df_hotspots.iterrows():
        sent_key = f"email_sent_{idx}"

        with st.container(border=True):
            st.subheader(f"🛠️ {row['Component']} Degradation Alert")
            subcol1, subcol2 = st.columns([1, 2])

            with subcol1:
                st.info(f"""
                **Assigned Response Team:**
                - **Team:** {row['Team']}
                - **Lead:** {row['FullName']}
                """)

            with subcol2:
                st.markdown("**🚨 Underlying Sensor Triggers (Root Causes):**")
                causes = row['CausesList']
                for c in causes:
                    # CauseMetadata may be a dataclass instance or a dict depending on load path
                    sensor = c.sensor if hasattr(c, 'sensor') else c['sensor']
                    code   = c.code   if hasattr(c, 'code')   else c['code']
                    related = c.related if hasattr(c, 'related') else c['related']
                    st.error(f"**{sensor}** — Code: `{code}` | Related: `{related}`", icon="⚠️")

            st.divider()

            # When clicked, add to the resolved lists and instantly rerun.
            # The row will be visually removed from the app on reload.
            if st.button(f"✉️ Page {row['FullName']} & Send Diagnostic Report", key=f"email_{idx}", use_container_width=True):
                logger.info("Routing diagnostic report to %s (%s)", row['FullName'], row['Team'])
                
                # Append the target component to the fixed list
                if "resolved_components" in st.session_state:
                    st.session_state["resolved_components"].append(row['Component'])
                    
                # Append all originating root causes linked to this hotspot
                if "resolved_sensors" in st.session_state:
                    for c in causes:
                        sensor = c.sensor if hasattr(c, 'sensor') else c['sensor']
                        st.session_state["resolved_sensors"].append(sensor)
                
                st.toast(f"Critical report successfully routed to {row['FullName']}!", icon="✅")
                st.rerun()
