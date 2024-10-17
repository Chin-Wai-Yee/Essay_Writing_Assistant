import streamlit as st
import jwt
import datetime

SECRET_KEY = st.secrets["JWT_SECRET_KEY"]

def generate_jwt(user_id, username):
    """Generate a JWT token."""
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt_token(token):
    """Verify a JWT token and return the user ID if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        st.error("Token has expired. Please log in again.")
        return None
    except jwt.InvalidTokenError:
        st.error("Invalid token. Please log in again.")
        return None

def logout():
    del st.session_state["jwt_token"]
    st.rerun()

def login_required(protected_page):
    def wrapper():
        if "jwt_token" not in st.session_state:
            st.error("You need to login to view this page")
            if st.button("Login/Register"):
                st.switch_page("pages/6_Profile.py")

            st.stop()

        user_id = verify_jwt_token(st.session_state["jwt_token"])
        if user_id:
            protected_page()
        else:
            del st.session_state["jwt_token"]
            st.rerun()
    return wrapper

def home_page():
    st.title("Home")
    st.write("Welcome to the home page. This page is accessible to all users.")

# @login_required
# def protected_page():
#     st.title("Protected Page")
#     st.write("This is a protected page. Only logged-in users can see this content.")

# @login_required
# def another_protected_page():
#     st.title("Another Protected Page")
#     st.write("This is another protected page. It's also only accessible to logged-in users.")