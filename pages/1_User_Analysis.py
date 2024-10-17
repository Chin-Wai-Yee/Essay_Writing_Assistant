from PIL import Image
import docx2txt
import PyPDF2
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="User Analysis", page_icon="🔍")

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_genai_connection

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

model = genai.GenerativeModel("gemini-1.5-flash",
                            system_instruction="""
You are a teahcer who are able to help learners to succeed in the essay writing especially in English Language.
The learner will have their input in the form of file, image or text. 
You will check the file, image or text and give the output with the strengths and weaknesses based on the essay that they have given. 
In addition, you have to determnine which type of essay that is suitable to them. 
The type of essay would be narraitve, argumentative, expository, and persuasive. 
Just give the output in the form of strengths and weaknesses of the user based on the files given not for the essay and also the type of essay that is suitable to the user.
""")


def get_user_analysis(files):

    response = model.generate_content(files)

    return response.text

def read_file_content(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type in ['jpg', 'jpeg', 'png']:
        return Image.open(uploaded_file), file_type
    
    elif file_type == 'txt':
        return uploaded_file.getvalue().decode('utf-8'), file_type
    
    elif file_type in ['doc', 'docx']:
        return docx2txt.process(uploaded_file), file_type
    
    elif file_type == 'pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text, file_type
    
    else:
        return "Unsupported file type", "unsupported"

uploaded_files = st.file_uploader(
    "Choose your files",
    type=["jpg", "jpeg", "png", "txt", "doc", "docx", "pdf"],
    accept_multiple_files=True
)

if uploaded_files is not None and st.button("Analyze"):

    files = []
    for file in uploaded_files:
        file_content, file_type = read_file_content(file)
        if file_type != "unsupported":
            files.append(file_content)
    with st.spinner("Analyzing..."):
        response = get_user_analysis(files)

    st.markdown(response)
