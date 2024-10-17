import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

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

def display_scores_over_time(user_entries, selected_username):
    # Create a DataFrame to hold scores over time
    scores_over_time = pd.DataFrame()

    for _, entry in user_entries.iterrows():
        scores = entry['suggestions']['essay_score']['scores']
        timestamp = entry['timestamp']
        
        # Create a temporary DataFrame for current entry's scores
        temp_df = pd.DataFrame(list(scores.items()), columns=['Category', 'Score'])
        temp_df['Timestamp'] = timestamp
        scores_over_time = pd.concat([scores_over_time, temp_df], ignore_index=True)

    # Plotting the scores over time using Plotly
    fig = px.line(scores_over_time, x='Timestamp', y='Score', color='Category',
                  labels={'Score': 'Scores', 'Timestamp': 'Date'},
                  title='Scores Over Time for {}'.format(selected_username),
                  markers=True)

    # Show the figure in Streamlit
    st.plotly_chart(fig)