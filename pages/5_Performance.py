import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Performance", page_icon="📊")

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_collection
from Authentication import login_required
from Data_Visualization import display_suggestion, display_user_analysis, display_scores_over_time

st.write("# Performance 📊")

def display_suggestion(suggestions):

    # Display essay type
    st.header("Essay Type")
    st.write(suggestions["essay_score"]["type_of_essay"])

    scores = suggestions['essay_score']['scores']
    scores_df = pd.DataFrame(list(scores.items()), columns=['Category', 'Score'])
    # Prepare data for the histogram
    scores_df['Category'] = scores_df['Category'].map(lambda x: x.replace('_', ' ').title())

    fig = px.bar(scores_df, y='Category', x='Score', color='Score',
             labels={'Score': 'Scores', 'Category': 'Score Categories'},
             title='Essay Evaluation Scores',
             text='Score')

    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis=dict(range=[0, 10]))

    st.header("Scores")
    # Show the figure in Streamlit
    st.plotly_chart(fig)

    # Display scores
    scores_df["Score"] = scores_df["Score"].map("{}/10".format)
    st.dataframe(scores_df, use_container_width=True, hide_index=True)

    # Display suggestions
    st.header("Suggestions")
    for s in suggestions["essay_score"]["essay_suggestion"]:
        with st.expander(f"Section {s['section']}"):
            st.subheader("Original Text")
            st.write(s["original_text"])
            st.subheader("Suggestion")
            st.write(s["suggestion"])
            st.subheader("Improved Version")
            st.write(s["improved_version"])

def display_user_analysis(user_analysis):
    # Display writing style and role
    st.header("Writing Style and Role")
    st.write(f"**Role:** {user_analysis['game_like_role']}")
    st.write(f"**Writing Style:** {user_analysis['writing_style']}")

    # Display strengths
    st.header("Strengths")
    for strength in user_analysis["strengths"]:
        st.write(f"- {strength}")

    # Display weaknesses
    st.header("Weaknesses")
    for weakness in user_analysis["weaknesses"]:
        st.write(f"- {weakness}")

    # Create a pie chart for strengths and weaknesses
    categories = ['Strengths', 'Weaknesses']
    values = [len(user_analysis["strengths"]), len(user_analysis["weaknesses"])]

    plt.figure(figsize=(4, 4))  # Adjust the size to be smaller
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'salmon'])
    plt.title('Strengths vs. Weaknesses')

    st.pyplot(plt)

# Function to retrieve past performance
def get_past_performance(username):
    return list(get_collection("user_performance").find({"username": username}).sort("timestamp", -1))

# Function to retrieve latest user analysis
def get_user_analysis(username):
    return get_collection("user_analysis").find_one({"username": username}, sort=[( '_id', -1 )])

@login_required
def main():

    tab1, tab2, tab3= st.tabs(["Overall Performance", "User Analysis", "Past Performance"])

    # Display past performance and analysis
    username = st.session_state["user"]["username"]
    # Filter entries for the selected username
    past_performance = get_past_performance(username)
    user_analysis = get_user_analysis(username)

    with tab1:
        user_entries = get_past_performance(username)

        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(user_entries)

        # Ensure timestamp is in datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Display scores over time
        display_scores_over_time(df, username)

    # Select a specific entry based on timestamp
    with tab2:
        if user_analysis:
            st.write("### Latest User Analysis")
            display_user_analysis(user_analysis['user_info'])
        else:
            st.write("No user analysis available.")
            if st.button("Go to User Analysis"):
                st.switch_page("1_User Analysis.py")

    with tab3:
        if past_performance:
            selected_entry_index = st.selectbox(
                "Select an entry",
                [f"{i+1} - {past_performance[i]['timestamp']}" for i in range(len(past_performance))],
            )
            index = int(selected_entry_index.split(" - ")[0]) - 1
            selected_entry = past_performance[index]
            st.write("### Selected Entry")
            display_suggestion(selected_entry["suggestions"])
        else:
            st.write("No past performance available.")
            if st.button("Go to Essay Suggestion"):
                st.switch_page("2_Essay_Suggestion.py")

main()