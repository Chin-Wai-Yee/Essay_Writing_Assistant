import streamlit as st

st.set_page_config(page_title="Essay Writing Chat", page_icon="💬")

st.write("# Essay Writing Chat 💬")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like help with in your essay?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Here you would typically use an AI model or API to generate responses
    # For this example, we'll just provide some generic responses
    response = "Here are some suggestions for your essay:\n\n" \
               "1. Make sure your thesis statement is clear and concise.\n" \
               "2. Use topic sentences to introduce each paragraph.\n" \
               "3. Provide evidence to support your arguments.\n" \
               "4. Use transitional phrases to connect your ideas.\n" \
               "5. Proofread your essay for grammar and spelling errors."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})