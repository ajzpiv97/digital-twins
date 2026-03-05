import streamlit as st

def _resolve_project_id(px, project_name: str) -> str | None:
    """
    Resolves the project ID for the given project name by calling px.list_projects().
    Result is cached in st.session_state to avoid repeated API calls.
    """
    cache_key = f"pmtx_project_id_{project_name}"

    if cache_key not in st.session_state:
        projects = px.list_projects()
        match = next((p for p in projects if p.get("name") == project_name), None)
        if match is None:
            available = [p.get("name") for p in projects]
            raise ValueError(
                f"Project '{project_name}' not found. "
                f"Available projects: {available}"
            )
        st.session_state[cache_key] = match["id"]

    return st.session_state[cache_key]


def render_refresh_button(settings):
    """
    Sidebar widget that triggers re-execution of Vadalog concepts
    via the prometheux_chain SDK, then clears Streamlit's data cache.
    Requires APP_ENV=platform to be set in the environment.
    """
    st.divider()
    st.markdown("**🔄 Refresh Analysis**")

    if settings.app_env != "platform":
        st.caption("🖥️ Running locally — data refresh requires `APP_ENV=platform`.")
        return

    configured = all([settings.pmtx_token, settings.pmtx_project])
    if not configured:
        st.caption("Configure `PMTX_TOKEN` and `PMTX_PROJECT` to enable live refresh.")
        return

    concepts_to_run = [
        (settings.concept_centrality, "Centrality Analysis"),
        (settings.concept_shortest_path, "Shortest Paths"),
        (settings.concept_hotspot, "Hotspot Metadata"),
    ]
    configured_concepts = [(cid, label) for cid, label in concepts_to_run if cid]

    if not configured_concepts:
        st.caption("No concept names configured.")
        return

    if st.button("🔄 Re-run Vadalog Programs", use_container_width=True):
        try:
            import prometheux_chain as px

            with st.spinner("Resolving project..."):
                project_id = _resolve_project_id(px, settings.pmtx_project)

            with st.spinner("Running Vadalog reasoning programs..."):
                for concept_name, label in configured_concepts:
                    with st.status(f"Running: {label}", expanded=False):
                        px.run_concept(project_id=project_id, concept_name=concept_name)
                        st.write(f"✅ {label} complete")

            st.cache_data.clear()
            st.success("✅ All programs complete. Dashboard will reload with fresh data.")
            st.rerun()

        except Exception as e:
            st.error(f"Refresh failed: `{e}`")
