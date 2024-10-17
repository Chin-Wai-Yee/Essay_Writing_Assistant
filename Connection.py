import streamlit as st
import pymongo
from openai import OpenAI
import google.generativeai as genai

MONGODB_URI = st.secrets["MONGODB_URI"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
GEMINIKEY = st.secrets["GOOGLE_API_KEY"]

# MongoDB connection (replace with your actual connection string)
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(MONGODB_URI)

def get_db():
    client = init_connection()
    return client["essay_assistant_db"]

def get_collection(collection_name):
    db = get_db()
    return db[collection_name]

@st.cache_resource
def get_openai_connection():
    client = OpenAI(api_key = OPENAI_API_KEY)
    return client

def get_genai_connection():
    genai.configure(api_key = GEMINIKEY)

# # Function to analyze essay and return results (placeholder)
# def analyze_essay(essay_text):
#     # Replace this with your actual essay analysis logic
#     return {
#         "score": 85,
#         "comments": "Good structure, but needs improvement in argumentation.",
#         "suggestions": [
#             "Strengthen your thesis statement",
#             "Provide more concrete examples",
#             "Improve transition between paragraphs"
#         ]
#     }

# # Function to analyze user's writing style (placeholder)
# def analyze_writing_style(essay_text):
#     # Replace this with your actual writing style analysis logic
#     return {
#         "style": "Analytical",
#         "vocabulary_level": "Advanced",
#         "sentence_complexity": "Moderate",
#         "common_themes": ["Technology", "Social issues"]
#     }

# # Streamlit UI
# st.title("Essay Submission and Analysis")

# user_id = st.text_input("Enter your user ID")
# essay_text = st.text_area("Paste your essay here")

# if st.button("Submit Essay"):
#     if user_id and essay_text:
#         # Analyze the essay
#         essay_analysis = analyze_essay(essay_text)
#         writing_style = analyze_writing_style(essay_text)
        
#         # Prepare performance data
#         performance_data = {
#             "user_id": user_id,
#             "essay_id": str(uuid.uuid4()),
#             "timestamp": datetime.now(),
#             "essay_text": essay_text,
#             "score": essay_analysis["score"],
#             "comments": essay_analysis["comments"],
#             "suggestions": essay_analysis["suggestions"]
#         }
        
#         # Insert performance data into MongoDB
#         performance_collection.insert_one(performance_data)
        
#         # Prepare user analysis data
#         analysis_data = {
#             "user_id": user_id,
#             "timestamp": datetime.now(),
#             "writing_style": writing_style
#         }
        
#         # Update user analysis in MongoDB
#         analysis_collection.update_one(
#             {"user_id": user_id},
#             {"$set": analysis_data},
#             upsert=True
#         )
        
#         st.success("Essay submitted and analyzed successfully!")
#         st.write("Essay Score:", essay_analysis["score"])
#         st.write("Comments:", essay_analysis["comments"])
#         st.write("Suggestions:", ", ".join(essay_analysis["suggestions"]))
#     else:
#         st.error("Please enter both user ID and essay text.")

# # Function to retrieve past performance
# def get_past_performance(user_id):
#     return list(performance_collection.find({"user_id": user_id}))

# # Function to retrieve latest user analysis
# def get_user_analysis(user_id):
#     return analysis_collection.find_one({"user_id": user_id})

# # Display past performance and analysis
# if st.button("View Past Performance"):
#     if user_id:
#         past_performance = get_past_performance(user_id)
#         user_analysis = get_user_analysis(user_id)
        
#         if past_performance:
#             st.write("Past Performance:")
#             for performance in past_performance:
#                 st.write(f"Date: {performance['timestamp']}")
#                 st.write(f"Score: {performance['score']}")
#                 st.write(f"Comments: {performance['comments']}")
#                 st.write("---")
#         else:
#             st.write("No past performance data found.")
        
#         if user_analysis:
#             st.write("User Writing Style Analysis:")
#             st.write(f"Style: {user_analysis['writing_style']['style']}")
#             st.write(f"Vocabulary Level: {user_analysis['writing_style']['vocabulary_level']}")
#             st.write(f"Sentence Complexity: {user_analysis['writing_style']['sentence_complexity']}")
#             st.write(f"Common Themes: {', '.join(user_analysis['writing_style']['common_themes'])}")
#         else:
#             st.write("No user analysis data found.")
#     else:
#         st.error("Please enter a user ID.")