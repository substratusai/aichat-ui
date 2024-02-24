import os

from openai import OpenAI
import streamlit as st


default_api_host = os.environ.get("API_HOST", "http://localhost:8080/v1")
default_model = os.environ.get("MODEL", "mixtral-8x7b-instruct-gptq")
default_api_key = os.environ.get("API_KEY", "Ignored by most backends. Can be anything.")

st.title("AI Chat UI")


if "messages" not in st.session_state:
    st.session_state.messages = []

def clear_messages():
    st.session_state.messages = []

with st.sidebar:
    st.title("Actions")
    st.button("Clear Chat", on_click=clear_messages)
    st.title("Settings")
    st.text_input("API Host", key="api_host", value=default_api_host)
    st.text_input("Model", key="model", value=default_model)
    st.text_input("API Key (Optional)", key="api_key", value=default_api_key)

client = OpenAI(api_key=st.session_state.api_key, base_url=st.session_state.api_host)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Remove the previous messages from user if there is no assist response in between
    i = len(st.session_state.messages) - 1
    while i >= 0:
        if st.session_state.messages[i]["role"] == "user":
            print("Popping")
            st.session_state.messages.pop(i)
        else:
            break
        i -= 1


    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})