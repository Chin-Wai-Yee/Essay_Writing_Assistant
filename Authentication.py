import streamlit as st
import pymongo
import bcrypt
from pymongo import MongoClient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json

# Initialize MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["user_auth_db"]
users_collection = db["users"]

# Google OAuth2 settings
CLIENT_CONFIG = {
    "web": {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["https://fictional-space-sniffle-j6pq567r49q2pgg7-8501.app.github.dev"],
    }
}

SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

# Streamlit app
def main():
    st.title("User Authentication App")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Register", "Login", "Guest", "Google Sign-In"])
    
    with tab1:
        st.header("Register")
        register_username = st.text_input("Username", key="reg_username")
        register_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            register_user(register_username, register_password)
    
    with tab2:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            login_user(login_username, login_password)
    
    with tab3:
        st.header("Guest")
        if st.button("Enter as Guest"):
            st.success("Welcome, Guest!")
            st.write("You have limited access as a guest.")
    
    with tab4:
        st.header("Google Sign-In")
        if st.button("Sign in with Google"):
            google_sign_in()

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        st.error("Username already exists. Please choose a different one.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_collection.insert_one({"username": username, "password": hashed_password})
        st.success("Registration successful! You can now log in.")

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        st.success(f"Welcome, {username}!")
        st.write("You have successfully logged in.")
    else:
        st.error("Invalid username or password. Please try again.")

def google_sign_in():
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=SCOPES
    )
    flow.redirect_uri = "https://fictional-space-sniffle-j6pq567r49q2pgg7-8501.app.github.dev"

    authorization_url, _ = flow.authorization_url(prompt="consent")

    st.markdown(f"[Click here to sign in with Google]({authorization_url})")

    # Check if the user has completed the Google sign-in process
    if 'code' in st.query_params:
        code = st.query_params['code'][0]
        flow.fetch_token(code=code)

        credentials = flow.credentials
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()

        # Store or update user information in MongoDB
        users_collection.update_one(
            {"email": user_info['email']},
            {"$set": {
                "name": user_info['name'],
                "picture": user_info['picture'],
                "google_id": user_info['id']
            }},
            upsert=True
        )

        st.success(f"Welcome, {user_info['name']}!")
        st.write("You have successfully signed in with Google.")
        st.image(user_info['picture'], width=100)

if __name__ == "__main__":
    main()