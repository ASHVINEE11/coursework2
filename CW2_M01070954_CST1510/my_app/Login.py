import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st
from auth import register_user, user_exists, login_user, validate_password, validate_username

st.set_page_config(page_title="Intellligence Platform", layout= "wide")
st.title("Login to Intelligence Platform")
st.write("Welcome! please log in or register.")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "tab" not in st.session_state:
    st.session_state.tab = "login"

tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    if not st.session_state.logged_in:
        st.subheader("Login")
    login_username = st.text_input("Username", key ="login_user")
    login_password = st.text_input("Password", type="password", key= "login_pass")

    if st.button("Log in"):
        if login_user(login_username, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome, {login_username}!")
            st.switch_page("pages/1_Cybersecurity.py")
        else:
            st.error("Invalid username or password")
    else:
        st.write(f"Welcome back, {st.session_state.username}")

        if st.button("Log out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

# --- REGISTER TAB ---
with tab_register:
    st.subheader("Register a new account")
    
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
    
    if st.button("Create account"):
        if not new_username or not new_password or not confirm_password:
            st.warning("Please fill in all fields.")
        elif not validate_username(new_username):
            st.warning("Invalid username. Must be 3-20 characters, letters & numbers only.")
        elif not validate_password(new_password):
            st.warning("Invalid password. Must be 8-50 characters long.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif user_exists(new_username):
            st.error("Username already exists.")
        else:
            register_user(new_username, new_password)
            st.success("Account created! 🎉")
            st.info("Switch to the Login tab to sign in.")




