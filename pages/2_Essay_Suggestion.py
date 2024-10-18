import sys
import os
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from File_handling import read_file_content
import google.generativeai as genai

st.set_page_config(page_title="Essay Suggestion", page_icon="💡")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_openai_connection, get_collection, get_genai_connection
from Data_Visualization import display_suggestion

st.write("# Get Essay Suggestions 💡")

# def get_essay_suggestions(essay, userinfo):

#     client = get_openai_connection()

#     system_prompt = (
# "You will be given an essay and the weaknesses and strengths of a student "
# "in writting an essay.\n"
# "Provide the score of the essay which ranged from 0 to 10.\n"
# "Then give some suggestion or improvement on the essay based on the weaknesses "
# "and strengths of the student.\n"
# "You can change some word or sentence of the essay to improve it.\n"
# "The output should be in JSON format:\n"
# """
# {
#     "essay_score": {
#         "type_of_essay": "Example Essay Type",
#         "scores": {
#         "content": ?,
#         "organization": ?,
#         "clarity_and_coherence": ?,
#         "grammar_and_language": ?,
#         "evidence_and_support": ?,
#         "conclusion": ?,
#         "overall_score": ?
#         },
#         "essay_suggestion": [
#         {
#             "section": 1,
#             "original_text": "Original text here...",
#             "suggestion": "Suggestion here...",
#             "improved_version": "Improved version here..."
#         },
#         {
#             "section": 2,
#             "original_text": "Original text here...",
#             "suggestion": "Suggestion here...",
#             "improved_version": "Improved version here..."
#         },
#         {
#             "section": 3,
#             "original_text": "Original text here...",
#             "suggestion": "Suggestion here...",
#             "improved_version": "Improved version here..."
#         }
#         ]
#     }
# }
# """.strip()
#     )

#     sample_essay = \
# """
# Having a healthy lifestyle is all about choosing to live your life in the most healthy way possible. There are a few things you have to do to start living your life in this way, i.e., the healthy way. This means doing some amount of exercise daily, such as jogging, yoga, playing sports, etc. Adding to this, you must also have a balanced and nutritional diet with all the food groups. It would be best if you were taking the right amount of proteins, carbohydrates, vitamins, minerals, and fats to help you have a proper diet. Grouped with these two essential aspects (diet and exercise), a healthy person also maintains the same sleep cycle, which should consist of around 7-8 hours of sleep.
# However, we must remember that a healthy lifestyle not only refers to our physical and mental health. Maintaining a balanced diet, exercising daily, and sleeping well are essential parts of a healthy lifestyle. But feeling happy is also a big part of a healthy lifestyle. To enable happiness, thinking positively is a must. When a person does not feel happy or good about themselves, they are not entirely healthy. Thus we must do our best to think positively so that we can feel happy rather than sad.
# We have talked about what all entails a healthy life, so now we must speak of what all does not. There are several things that one must avoid in order to live a healthy lifestyle. These include the kind of practices and habits that are harmful to us and also to the people around us, i.e., society. Such practices and habits include gambling, smoking, drinking, illegal drugs, or any other things that can turn into an addiction. These habits are harmful to not only you but for all the people around you, as addiction causes unhealthy attitudes and behaviors. Other unhealthy practices include skipping meals and eating junk food.
# The benefits of a healthy lifestyle are manifold: living a healthy life allows you to live longer, which means that you get to spend more time with your family. Exercising daily will enable you to release endorphins and helps you feel happier. Regular exercise also improves the health of your skin and hair, bettering your appearance as well. Healthy lifestyles also primarily reduce your risk of life-threatening diseases such as cancer, diabetes, etc. and also reduce your susceptibility to cardiac arrests.
# Overall, living your life in a healthy way only has benefits, and that’s why it is recommended that you do everything you can to have a healthy lifestyle. So, eat three nutritional meals a day, avoid unhealthy junk food, go for a run or jog in the morning, get your full 8 hours of sleep, and avoid bad habits like drugs, alcohol, and smoking. A healthy lifestyle is the best thing that you can do to your body, and you will be thanking yourself for following a healthy lifestyle in the later years of your life.
# """.strip()
#     sample_userinfo = (
#         "Strengths : Clear Message, Well-Organized, Comprehensive Content, "
#         "Encouraging Tone, Use of Specific Examples.\n"
#         "Weaknesses : Repetition, Vague Assertions, Lack of Evidence, "
#         "Generalized Conclusion, Sentence Structure, Transitions and Flow."
#     )

#     sample_answer = \
# """
# {
# "essay_evaluation": {
#     "type_of_essay": "Persuasive Essay",
#     "scores": {
#     "content": 7,
#     "organization": 7,
#     "clarity_and_coherence": 8,
#     "grammar_and_language": 8,
#     "evidence_and_support": 9,
#     "conclusion": 7,
#     "overall_score": 8
#     },
#     "feedback": [
#     {
#         "section": 1,
#         "original_text": "...",
#         "suggestion": "...",
#         "improved_version": "..."
#     },
#     {
#         "section": 2,
#         "original_text": "...",
#         "suggestion": "...",
#         "improved_version": "..."
#     },
#     {
#         "section": 3,
#         "original_text": "...",
#         "suggestion": "...",
#         "improved_version": "..."
#     }
#     ]
# }
# }
# """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Essay: {sample_essay}\n"
#                     f"UserInfo: {sample_userinfo}\n"
#                     "Please provide specific suggestions on "
#                     "how to improve the essay based on "
#                     "the provided user information."
#                 )
#             },
#             {
#                 "role": "assistant",
#                 "content": sample_answer
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Essay: {essay}\n"
#                     f"UserInfo: {userinfo}\n"
#                     "Please provide specific suggestions on "
#                     "how to improve the essay based on "
#                     "the provided user information."
#                 )
#             }
#         ]
#     )

#     return response.choices[0].message.content
def get_essay_suggestions(essay, userinfo):

    get_genai_connection()

    system_prompt = (
"You will be given an essay and the weaknesses and strengths of a student "
"in writting an essay.\n"
"Provide the score of the essay which ranged from 0 to 10.\n"
"Then give some suggestion or improvement on the essay based on the weaknesses "
"and strengths of the student.\n"
"You can change some word or sentence of the essay to improve it.\n"
"The output should be in JSON format:\n"
"""
{
    "essay_score": {
        "type_of_essay": "Example Essay Type",
        "scores": {
        "content": ?,
        "organization": ?,
        "clarity_and_coherence": ?,
        "grammar_and_language": ?,
        "evidence_and_support": ?,
        "conclusion": ?,
        "overall_score": ?
        },
        "essay_suggestion": [
        {
            "section": 1,
            "original_text": "Original text here...",
            "suggestion": "Suggestion here...",
            "improved_version": "Improved version here..."
        },
        {
            "section": 2,
            "original_text": "Original text here...",
            "suggestion": "Suggestion here...",
            "improved_version": "Improved version here..."
        },
        {
            "section": 3,
            "original_text": "Original text here...",
            "suggestion": "Suggestion here...",
            "improved_version": "Improved version here..."
        }
        ]
    }
}
""".strip()
    )

    sample_essay = \
"""
Having a healthy lifestyle is all about choosing to live your life in the most healthy way possible. There are a few things you have to do to start living your life in this way, i.e., the healthy way. This means doing some amount of exercise daily, such as jogging, yoga, playing sports, etc. Adding to this, you must also have a balanced and nutritional diet with all the food groups. It would be best if you were taking the right amount of proteins, carbohydrates, vitamins, minerals, and fats to help you have a proper diet. Grouped with these two essential aspects (diet and exercise), a healthy person also maintains the same sleep cycle, which should consist of around 7-8 hours of sleep.
However, we must remember that a healthy lifestyle not only refers to our physical and mental health. Maintaining a balanced diet, exercising daily, and sleeping well are essential parts of a healthy lifestyle. But feeling happy is also a big part of a healthy lifestyle. To enable happiness, thinking positively is a must. When a person does not feel happy or good about themselves, they are not entirely healthy. Thus we must do our best to think positively so that we can feel happy rather than sad.
We have talked about what all entails a healthy life, so now we must speak of what all does not. There are several things that one must avoid in order to live a healthy lifestyle. These include the kind of practices and habits that are harmful to us and also to the people around us, i.e., society. Such practices and habits include gambling, smoking, drinking, illegal drugs, or any other things that can turn into an addiction. These habits are harmful to not only you but for all the people around you, as addiction causes unhealthy attitudes and behaviors. Other unhealthy practices include skipping meals and eating junk food.
The benefits of a healthy lifestyle are manifold: living a healthy life allows you to live longer, which means that you get to spend more time with your family. Exercising daily will enable you to release endorphins and helps you feel happier. Regular exercise also improves the health of your skin and hair, bettering your appearance as well. Healthy lifestyles also primarily reduce your risk of life-threatening diseases such as cancer, diabetes, etc. and also reduce your susceptibility to cardiac arrests.
Overall, living your life in a healthy way only has benefits, and that’s why it is recommended that you do everything you can to have a healthy lifestyle. So, eat three nutritional meals a day, avoid unhealthy junk food, go for a run or jog in the morning, get your full 8 hours of sleep, and avoid bad habits like drugs, alcohol, and smoking. A healthy lifestyle is the best thing that you can do to your body, and you will be thanking yourself for following a healthy lifestyle in the later years of your life.
""".strip()
    sample_userinfo = (
        "Strengths : Clear Message, Well-Organized, Comprehensive Content, "
        "Encouraging Tone, Use of Specific Examples.\n"
        "Weaknesses : Repetition, Vague Assertions, Lack of Evidence, "
        "Generalized Conclusion, Sentence Structure, Transitions and Flow."
    )

    sample_answer = \
"""
{
"essay_evaluation": {
    "type_of_essay": "Persuasive Essay",
    "scores": {
    "content": 7,
    "organization": 7,
    "clarity_and_coherence": 8,
    "grammar_and_language": 8,
    "evidence_and_support": 9,
    "conclusion": 7,
    "overall_score": 8
    },
    "feedback": [
    {
        "section": 1,
        "original_text": "...",
        "suggestion": "...",
        "improved_version": "..."
    },
    {
        "section": 2,
        "original_text": "...",
        "suggestion": "...",
        "improved_version": "..."
    },
    {
        "section": 3,
        "original_text": "...",
        "suggestion": "...",
        "improved_version": "..."
    }
    ]
}
}
"""
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction = (
            system_prompt
        )
    )

    response = model.generate_content([f"Sample essay: {sample_essay}", f"Sample User Info: {sample_userinfo}",f"Sample output: {sample_answer}", essay, user_info])

    return response.text

# Function to add the reponse to collection
def add_to_collection(data):
    collection = get_collection("user_performance")
    collection.insert_one(data)

uploaded_file = st.file_uploader(
    "Upload your essay",
    type=["txt", "doc", "docx", "pdf"]
)

if uploaded_file:
    essay_content, file_type = read_file_content(uploaded_file)
    if file_type == "unsupported":
        st.write("Unsupported file type")
        st.stop()

    with st.expander("Uploaded Essay:"):
        st.markdown(essay_content)

    if st.button("Get Suggestions"):
        suggestions = ""
        user_info = ""
        if "user_info" in st.session_state:
            user_info = json.dumps(st.session_state["user_info"])

        with st.spinner("Generating suggestions..."):
            suggestions = get_essay_suggestions(
                essay_content, user_info
            )

        start = suggestions.find('{')
        end = suggestions.rfind('}') + 1
        suggestions = suggestions[start:end]
        suggestions_json = json.loads(suggestions)

        st.session_state["essay_suggestions"] = suggestions_json

        # If user is logged in, save the suggestions to the collection
        if "user" in st.session_state:
            user = st.session_state["user"]

            add_to_collection({
                "username": user["username"],
                "suggestions": suggestions_json,
                "timestamp": datetime.now()
            })

if "essay_suggestions" in st.session_state:
    display_suggestion(st.session_state["essay_suggestions"])