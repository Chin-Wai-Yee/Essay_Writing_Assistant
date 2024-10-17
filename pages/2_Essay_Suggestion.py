import streamlit as st

st.set_page_config(page_title="Essay Suggestion", page_icon="💡")

st.write("# Get Essay Suggestions 💡")

uploaded_file = st.file_uploader("Upload your essay", type=["txt", "doc", "docx", "pdf"])

if uploaded_file:
    essay_content = uploaded_file.read().decode()
    st.write("Essay content:")
    st.write(essay_content)
    
    if st.button("Get Suggestions"):
        # Here you would typically use an AI model or API to generate suggestions
        # For this example, we'll just provide some generic feedback
        suggestions = [
            "Consider revising your introduction to make it more engaging.",
            "Make sure your thesis statement is clear and concise.",
            "Try to vary your sentence structure for better flow.",
            "Check for any grammatical errors or typos.",
            "Ensure your conclusion summarizes your main points effectively."
        ]
        
        st.write("Suggestions:")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")