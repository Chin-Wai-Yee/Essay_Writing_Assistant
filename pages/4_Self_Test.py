import streamlit as st

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_collection, get_openai_connection
from Authentication import login_required

def main():
    st.title("Essay Writing Assistant")
    st.write("Please answer the following questions to help us understand you better and provide tailored essay writing assistance.")

    questions = [
        "What is your current occupation or field of study?",
        "What is your highest level of education?",
        "What is your primary language?",
        "How would you rate your English writing skills? (1-10)",
        "What type of essays do you usually write? (e.g., academic, personal, professional)",
        "What subjects are you most interested in or knowledgeable about?",
        "Do you have any specific areas where you struggle with essay writing?",
        "How often do you write essays?",
        "What is your preferred writing style? (e.g., formal, casual, technical)",
        "Do you have any upcoming essay deadlines or specific topics you need help with?"
    ]

    # Initialize session state to keep track of the current question and responses
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        response = st.text_input(f"{st.session_state.current_question + 1}. {question}", key=f"q{st.session_state.current_question}")
        
        if st.button("Next" if st.session_state.current_question < len(questions) - 1 else "Submit"):
            st.session_state.responses[f"Q{st.session_state.current_question + 1}"] = response
            st.session_state.current_question += 1
            st.rerun()
    else:
        system_prompt = (
            "You are a teacher who analyzes students' writing styles "
            "based on their responses to a series of questions. "
            "You will provide a summary of their responses in not more than 100 words. "
        )
        with st.spinner("Processing your responses..."):

            client = get_openai_connection()

            prompt = ""
            for q, a in st.session_state.responses.items():
                prompt += (f"{q}: {a}")

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=100
            )

            summary = response.choices[0].text

        st.write("Thank you for providing your information. Here's a summary of your responses:")
        
        st.markdown(summary)

        if st.button("Start Over"):
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.rerun()

if __name__ == "__main__":
    main()