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

            # Persist sent state so confirmation doesn't vanish on next rerun
            if st.session_state.get(sent_key):
                st.success(f"Diagnostics payload transmitted to the **{row['Team']}** operations channel.")
            elif st.button(f"✉️ Page {row['FullName']} & Send Diagnostic Report", key=f"email_{idx}"):
                logger.info("Routing diagnostic report to %s (%s)", row['FullName'], row['Team'])
                st.session_state[sent_key] = True
                st.toast(f"Critical report successfully routed to {row['FullName']}!", icon="✅")
                st.rerun()
