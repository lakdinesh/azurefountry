import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Enterprise Support Agent",
    layout="wide"
)

st.title("🤖 Enterprise Support Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("Ask support question...")

if user_question:
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_question},
                    timeout=90
                )

                response.raise_for_status()
                data = response.json()

                answer = data["answer"]

                st.markdown(answer)

                with st.expander("Trace details"):
                    st.write("Sources:", data.get("sources", []))
                    st.write("Latency ms:", data.get("latency_ms"))
                    st.write("Tokens:", data.get("tokens", {}))

            except Exception as e:
                answer = f"Error: {str(e)}"
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })