# Home.py
import streamlit as st

st.set_page_config(page_title="Essay Assistant Home", page_icon="🏠")

st.write("# Welcome to the Essay Assistant! 📝")

st.write("Choose a page to navigate:")

col1, col2 = st.columns(2)

with col1:
    if st.button("User Analysis", use_container_width=True):
        st.switch_page("pages/1_User_Analysis.py")
    
    if st.button("Essay Suggestion", use_container_width=True):
        st.switch_page("pages/2_Essay_Suggestion.py")

with col2:
    if st.button("Essay Writing Chat", use_container_width=True):
        st.switch_page("pages/3_Essay_Writing_Chat.py")

    if st.button("Performance", use_container_width=True):
        st.switch_page("pages/5_Performance.py")
    
    # Add more buttons here if you have additional pages