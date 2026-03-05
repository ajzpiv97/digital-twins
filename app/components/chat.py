import streamlit as st
import requests

CHAT_API_URL = "https://chat-docs.prometheux.ai/api/docsChat"

def _stream_prometheux_response(messages: list[dict]):
    """
    Generator that streams tokens from the Prometheux Chat API.
    Parses the AI SDK wire format: 0:"token"
    """
    payload = {"messages": messages}
    with requests.post(CHAT_API_URL, json=payload, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        for chunk in resp.iter_content(chunk_size=512, decode_unicode=True):
            if not chunk:
                continue
            for line in chunk.split("\n"):
                line = line.strip()
                # AI SDK format: 0:"token"
                if line.startswith('0:"') and line.endswith('"'):
                    yield line[3:-1].replace("\\n", "\n")


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

        # Only send the last 10 messages to keep context window manageable
        context = st.session_state.messages[-10:]

        with st.chat_message("assistant"):
            try:
                response_text = st.write_stream(_stream_prometheux_response(context))
            except Exception as e:
                response_text = f"⚠️ Could not reach the Prometheux Chat API: `{e}`"
                st.warning(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})