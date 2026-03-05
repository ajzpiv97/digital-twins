import streamlit as st
import requests
import re
import logging

try:
    from digital_twin.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    logger = logging.getLogger(__name__)

CHAT_API_URL = "https://chat-docs.prometheux.ai/api/docsChat"

def _get_prometheux_response(messages: list[dict]) -> str:
    logger.info("Calling Prometheux Chat API — %d messages in context", len(messages))
    payload = {"messages": messages}
    resp = requests.post(CHAT_API_URL, json=payload, stream=True, timeout=60)
    resp.raise_for_status()

    raw = resp.text
    logger.debug("Raw API response length: %d chars", len(raw))

    tokens = re.findall(r'0:"((?:[^"\\]|\\.)*)"', raw)
    if tokens:
        logger.debug("Parsed %d AI SDK tokens", len(tokens))
        return "".join(tokens).replace("\\n", "\n").replace('\\"', '"')

    # Fallback: strip data: prefixes
    logger.warning("AI SDK token format not matched — falling back to plain text extraction")
    lines = [l.removeprefix("data:").strip() for l in raw.splitlines() if l.strip() and not l.strip().startswith("[")]
    return "\n".join(lines) if lines else raw.strip()



def render_chat_interface():
    st.subheader("💬 Prometheux Assistant")
    st.markdown("Ask about the engine topology, failure chains, or Vadalog reasoning.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System online. Ask me about the engine topology, centrality scores, or failure propagation paths."}
        ]

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # React to user input
    if prompt := st.chat_input("Ask about failure paths, hotspots, or Vadalog..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        context = st.session_state.messages[-10:]

        with st.chat_message("assistant"):
            with st.spinner("Querying Prometheux..."):
                try:
                    response_text = _get_prometheux_response(context)
                    st.markdown(response_text)
                except Exception as e:
                    response_text = f"⚠️ Could not reach the Prometheux Chat API: `{e}`"
                    st.warning(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})