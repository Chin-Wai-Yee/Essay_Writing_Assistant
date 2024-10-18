import bcrypt
import sys, os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from bson import ObjectId

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Connection import get_collection
from Authentication import generate_jwt, verify_jwt_token, logout

# Initialize MongoDB connection
users_collection = get_collection("users")

def login_page():
    tab1, tab2 = st.tabs(["Register", "Login"])

    with tab1:
        register_tab()

    with tab2:
        login_tab()

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
    user = users_collection.find_one({'username': username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        user_id = str(user['_id'])
        st.session_state['jwt_token'] = generate_jwt(user_id, username)
        st.session_state['user'] = user
        st.rerun()
    else:
        st.error("Invalid username or password. Please try again.")

@st.cache_data(ttl=600)
def get_user(_user_id):
    return users_collection.find_one({"_id": _user_id})

def user_profile(user_id):

    _user_id = ObjectId(user_id)

    if "user" not in st.session_state:
        st.session_state.user = user
    else:
        user = get_user(_user_id)

    # st.write(f"User ID: {user['_id']}")
    st.write(f"Hi, {user['username']}")
    st.image(user['picture'], width=100)
    st.write(f"Email: {user['email']}")

    if st.button("Logout"):
        logout()

st.title("User Authentication System")
if "jwt_token" not in st.session_state:
    login_page()
else:
    user_id = verify_jwt_token(st.session_state["jwt_token"])
    if user_id:
        user_profile(user_id)
    else:
        del st.session_state["jwt_token"]
        st.experimental_rerun()