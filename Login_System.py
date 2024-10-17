import streamlit as st
import bcrypt
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
from Connection import get_collection
from Authentication import generate_jwt, verify_jwt_token, logout
from bson import ObjectId

# Initialize MongoDB connection
users_collection = get_collection("users")

# Google OAuth2 settings
redirect_uri = "https://your_redirect_uri"
CLIENT_CONFIG = {
    "web": {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [redirect_uri],
    }
}
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

def login_page():
    tab1, tab2, tab3 = st.tabs(["Register", "Login", "Google Sign-In"])

    with tab1:
        register_tab()

    with tab2:
        login_tab()

    with tab3:
        google_sign_in_tab()

def register_tab():
    st.header("Register")
    register_username = st.text_input("Username", key="reg_username")
    register_email = st.text_input("Email", key="reg_email")
    register_password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register"):
        register_user(register_username, register_email, register_password)

def login_tab():
    st.header("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        login_user(login_username, login_password)

def google_sign_in_tab():
    st.header("Google Sign-In")
    google_sign_in()

def register_user(username, email, password):
    if not username or not email or not password:
        st.error("Please fill in all the fields.")
    elif users_collection.find_one({"username": username}):
        st.error("Username already exists. Please choose a different one.")
    elif users_collection.find_one({"email": email}):
        st.error("Email already exists. Please choose a different one.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_collection.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "email": email,
                "picture": "https://www.shutterstock.com/image-vector/blank-avatar-photo-place-holder-600nw-1114445501.jpg"
            }
        )
        st.success("Registration successful! You can now log in.")

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        user_id = str(user['_id'])
        st.session_state["jwt_token"] = generate_jwt(user_id)
        st.rerun()
    else:
        st.error("Invalid username or password. Please try again.")

def google_sign_in():
    flow = Flow.from_client_config(client_config=CLIENT_CONFIG, scopes=SCOPES)
    flow.redirect_uri = redirect_uri
    authorization_url, _ = flow.authorization_url(prompt="consent")
    st.warning("This feature is under development. Please use the Register and Login tabs.")
    st.link_button("Login with Google", authorization_url)

    if 'code' in st.query_params:
        code = st.query_params['code'][0]
        flow.fetch_token(code=code)
        credentials = flow.credentials
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        users_collection.update_one({"email": user_info['email']}, {"$set": {"name": user_info['name'], "picture": user_info['picture'], "google_id": user_info['id']}}, upsert=True)
        st.success(f"Welcome, {user_info['name']}!")
        st.image(user_info['picture'], width=100)

@st.cache_data(ttl=600)
def get_user(_user_id):
    return users_collection.find_one({"_id": _user_id})

def user_info(user_id):

    if st.button("Logout"):
        logout()

    _user_id = ObjectId(user_id)
    user = get_user(_user_id)
    st.write(f"User ID: {user['_id']}")
    st.write(f"Username: {user['username']}")
    st.write(f"Email: {user['email']}")
    st.image(user['picture'], width=100)

st.title("User Authentication System")
if "jwt_token" not in st.session_state:
    login_page()
else:
    user_id = verify_jwt_token(st.session_state["jwt_token"])
    if user_id:
        user_info(user_id)
    else:
        del st.session_state["jwt_token"]
        st.experimental_rerun()