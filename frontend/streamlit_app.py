import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="Enterprise AI Agent",
    layout="wide"
)

st.title("🤖 Enterprise Support Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_question = st.chat_input("Ask me anything...")

if user_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    response = requests.post(
        API_URL,
        json={
            "message": user_question
        }
    )

    answer = response.json()["answer"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)