import streamlit as st

st.set_page_config(page_title="Essay Writing Chat", page_icon="💬")

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_openai_connection

st.write("# Essay Writing Chat 💬")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """"You are an essay teacher and will be 
            asked some question related to essay writing. 
            Answer the question that related to essay writing.
            If the question is not related to essay writing, answer with "Sorry, I can  
            only answer the question related to essay writing. Please ask again."
            you can generate the sample of the essay type or the essay based on the structure given if you have been told to do so
         ."""},
        {"role": "assistant", "content": "Hello! I'm here to help you with your essay. What would you like to know?"}
    ]

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = get_openai_connection()

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})