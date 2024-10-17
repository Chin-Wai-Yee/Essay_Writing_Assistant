import streamlit as st

st.set_page_config(page_title="User Analysis", page_icon="🔍")

st.write("# Welcome to the Essay Assistant! 🔍")

st.markdown(
    """
    This Essay Assistant app helps you improve your writing skills:
    
    - **Home Page**: Upload your files here
    - **Essay Suggestion**: Get suggestions on your uploaded essay
    - **Essay Writing Chat**: Chat with an AI assistant while writing your essay
    
    To get started, upload your files below:
"""
)

uploaded_files = st.file_uploader("Choose your files", accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        file_contents = file.read()
        st.write(f"Filename: {file.name}")
        st.write(f"File size: {file.size} bytes")
        # You can process the file contents here or save them for use in other pages