import streamlit as st
import logging

try:
    from digital_twin.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    logger = logging.getLogger(__name__)


def _resolve_project_id(px, project_name: str) -> str | None:
    """
    Resolves the project ID for the given project name by calling px.list_projects().
    Result is cached in st.session_state to avoid repeated API calls.
    """
    cache_key = f"pmtx_project_id_{project_name}"

    if cache_key not in st.session_state:
        logger.info("Resolving project ID for: '%s'", project_name)
        projects = px.list_projects()
        logger.debug("Found %d projects on platform", len(projects))
        match = next((p for p in projects if p.get("name") == project_name), None)
        if match is None:
            available = [p.get("name") for p in projects]
            logger.error("Project '%s' not found. Available: %s", project_name, available)
            raise ValueError(
                f"Project '{project_name}' not found. "
                f"Available projects: {available}"
            )
        st.session_state[cache_key] = match["id"]
        logger.info("Resolved project ID: %s", match["id"])
    else:
        logger.debug("Using cached project ID for '%s'", project_name)

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
        if st.button("🔄 Reset Local Simulation State", use_container_width=True):
            st.session_state["resolved_components"] = []
            st.session_state["resolved_sensors"] = []
            st.rerun()
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
                        logger.info("Running concept: %s (project_id=%s)", concept_name, project_id)
                        px.run_concept(project_id=project_id, concept_name=concept_name)
                        logger.info("Concept complete: %s", concept_name)
                        st.write(f"✅ {label} complete")

            logger.info("All concepts complete — clearing data cache")
            st.cache_data.clear()
            st.session_state["resolved_components"] = []
            st.session_state["resolved_sensors"] = []
            
            import datetime
            from pathlib import Path
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(Path.cwd() / "last_run.txt", "w") as f:
                f.write(now_str)
                
            st.success("✅ All programs complete. Dashboard will reload with fresh data.")
            st.rerun()

        except Exception as e:
            logger.exception("Refresh failed: %s", e)
            st.error(f"Refresh failed: `{e}`")
