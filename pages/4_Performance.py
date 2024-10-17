import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Performance", page_icon="📊")

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_collection

st.write("# Performance 📊")

# Function to generate sample data (replace this with actual data retrieval)
def get_sample_data():
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    scores = [75 + i % 10 for i in range(30)]  # Scores between 75 and 84
    return pd.DataFrame({'Date': dates, 'Score': scores})

# Get the data
df = get_sample_data()

# Create the graph
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Score'], mode='lines+markers'))
fig.update_layout(
    title='Essay Performance Over Time',
    xaxis_title='Date',
    yaxis_title='Essay Score',
    yaxis_range=[0, 100]
)

# Display the graph
st.plotly_chart(fig)

# Allow user to view past reports
st.write("## Past Performance Reports")

# Simulating past reports (replace this with actual report retrieval)
past_reports = {
    "May 2023": "Your essays showed significant improvement in structure and argumentation.",
    "June 2023": "Grammar and vocabulary usage have enhanced, but thesis statements need more clarity.",
    "July 2023": "Excellent progress in developing complex ideas. Focus on improving conclusions."
}

selected_report = st.selectbox("Select a report to view", list(past_reports.keys()))

if selected_report:
    st.write(f"### Report for {selected_report}")
    st.write(past_reports[selected_report])

# Provide an option to download the full report (simulated)
if st.button("Download Full Report"):
    # In a real application, you would generate and provide a downloadable report here
    st.write("Downloading full report... (This is a placeholder for the actual download functionality)")

# Add a section for setting goals
st.write("## Set Performance Goals")
goal_score = st.slider("Set your target essay score", min_value=0, max_value=100, value=85)
st.write(f"Your current goal: Achieve a consistent essay score of {goal_score} or higher.")

# Provide personalized recommendations based on the current performance
average_score = df['Score'].mean()
if average_score < goal_score:
    st.write(f"To reach your goal of {goal_score}, consider focusing on:")
    st.write("- Improving essay structure and organization")
    st.write("- Enhancing vocabulary and language use")
    st.write("- Strengthening your argumentation and evidence")
else:
    st.write("Great job! You're consistently meeting or exceeding your goal. Consider setting a higher target to continue improving.")

# Function to retrieve past performance
def get_past_performance(user_id):
    return list(get_collection("user_performance").find({"user_id": user_id}))

# Function to retrieve latest user analysis
def get_user_analysis(user_id):
    return get_collection("user_analysis").find_one({"user_id": user_id})

# Display past performance and analysis
user_id = st.text_input("Enter your user ID")
if st.button("View Past Performance"):
    if user_id:
        past_performance = get_past_performance(user_id)
        user_analysis = get_user_analysis(user_id)
        
        if past_performance:
            st.write("Past Performance:")
            for performance in past_performance:
                st.write(f"Date: {performance['timestamp']}")
                st.write(f"Score: {performance['score']}")
                st.write(f"Comments: {performance['comments']}")
                st.write("---")
        else:
            st.write("No past performance data found.")
        
        if user_analysis:
            st.write("User Writing Style Analysis:")
            st.write(f"Style: {user_analysis['writing_style']['style']}")
            st.write(f"Vocabulary Level: {user_analysis['writing_style']['vocabulary_level']}")
            st.write(f"Sentence Complexity: {user_analysis['writing_style']['sentence_complexity']}")
            st.write(f"Common Themes: {', '.join(user_analysis['writing_style']['common_themes'])}")
        else:
            st.write("No user analysis data found.")
    else:
        st.error("Please enter a user ID.")