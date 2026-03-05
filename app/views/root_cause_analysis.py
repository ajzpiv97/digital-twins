import streamlit as st

def render_root_cause_analysis(df_hotspots):
    st.header("🔍 Root Cause Analysis & Personnel Routing")
    st.markdown("Immediate safety and operational actions automatically traced to responsible engineering teams.")
    
    if df_hotspots is not None and not df_hotspots.empty:
        for idx, row in df_hotspots.iterrows():
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
                        st.error(f"**{c['sensor']}** — Code: `{c['code']}` | Related: `{c['related']}`", icon="⚠️")
                
                st.divider()
                if st.button(f"✉️ Page {row['FullName']} & Send Diagnostic Report", key=f"email_{idx}"):
                    st.toast(f"Critical report successfully routed to {row['FullName']}!", icon="✅")
                    st.success(f"Diagnostics payload transmitted to the **{row['Team']}** operations channel.")
    else:
        st.info("No active hotspots currently demanding attention.")
