import os
import sys
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Essay Writing Chat", page_icon="💬")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_openai_connection, get_genai_connection

st.write("# Essay Writing Chat 💬")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    system_prompt = (
        "You are an essay teacher and will be answering "
        "only question that related to essay writing. "
        "You can write a sample essay based on a type or any topic "
        "or based a given structure. "
        "If a question is not related to essay writing, "
        "do not answer it and provide your reasons."
    )
    if "user_info" in st.session_state:
        system_prompt += "\nFollowing is some info about your student:\n"
        system_prompt += "\n".join(
            f"- {k}: {v}" for k, v in st.session_state.user_info.items()
        )
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "assistant",
            "content": "Hello, I am your essay teacher, "
            "how can I help you?",
        }
    ]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = get_openai_connection()

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # stream = client.chat.completions.create(
        #     model=st.session_state["openai_model"],
        #     messages=[
        #         {"role": m["role"], "content": m["content"]}
        #         for m in st.session_state.messages
        #     ],
        #     stream=True,
        # )
        
        # Gemini
        get_genai_connection()
        system_prompt = (
            "You are an essay teacher and will be answering "
            "only question that related to essay writing. "
            "You can write a sample essay based on a type or any topic "
            "or based a given structure. "
            "If a question is not related to essay writing, "
            "do not answer it and provide your reasons."
        )
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction = (
                system_prompt
            )
        )

        stream = model.generate_content(
            [
                f'role": {m["role"]}, "content": {m["content"]}'
                for m in st.session_state.messages
            ]
        ).text

        st.write(stream)
        # response = st.write_stream(stream)
    st.session_state.messages.append(
        {"role": "assistant", "content": stream}
    )
    # st.session_state.messages.append(
    #     {"role": "assistant", "content": response}
    # )
