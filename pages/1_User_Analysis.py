import json
import os
import sys
import datetime
import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
from File_handling import read_file_content

st.set_page_config(page_title="User Analysis", page_icon="🔍")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_collection, get_genai_connection
from Data_Visualization import display_user_analysis

st.write("# Welcome to the User Analysis! 🔍")

st.markdown(
    """
    This tool will analyze the your writing style.  
    To get started, upload your files below:
    """
)

get_genai_connection()
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction = (
"You are a teahcer who are able to help learners to "
"succeed in the essay writing especially in English Language. "
"The learner will have their input in the form of file, image or text. "
"You will check the file, image or text and give the output "
"with the strengths and weaknesses based on the essay that they have given. "
"In addition, you have to determnine which type of essay that is suitable to them. "
"The type of essay would be narraitve, argumentative, expository, and persuasive.\n"
"The output should be JSON format with the "
"strengths, weaknesses, writing_style of user, "
"a game-like role that describes the user's writing style.\n"
"don't mention json like '```json' in output"
"""
Example:
{
    "strengths": ["Good grammar", "Strong arguments"],
    "weaknesses": ["Poor structure", "Weak conclusion"],
    "writing_style": "Argumentative"
    "game_like_role": "The Persuader"
}
""".strip())   
)

def get_user_analysis(files):
    response = model.generate_content(files)
    return response.text

def update_user_info(response):

    st.session_state["user_analysis"] = response

    if "user" not in st.session_state:
        return

    user = st.session_state["user"]
    user_analysis_collection = get_collection("user_analysis")

    new_user_info = {
        "username": user["username"],
        "user_info": response,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    user_analysis_collection.insert_one(new_user_info)

uploaded_files = st.file_uploader(
    "Choose your files",
    type=["jpg", "jpeg", "png", "txt", "doc", "docx", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if not st.button("Analyze"):
        st.stop()

    files = []
    for file in uploaded_files:
        file_content, file_type = read_file_content(file)
        if file_type != "unsupported":
            files.append(file_content)
        else:
            st.error(f"Unsupported file type: {file.name}")

    invalid_json = True
    while invalid_json:
        with st.spinner("Analyzing... This may take some times..."):
            response = get_user_analysis(files)
            start = response.find('{')
            end = response.rfind('}') + 1
            response = response[start:end]
        try:
            response_json = json.loads(response)
            invalid_json = False
        except json.JSONDecodeError:
            pass

    update_user_info(response_json)

if "user_analysis" in st.session_state:
    display_user_analysis(st.session_state["user_analysis"])