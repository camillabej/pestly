import streamlit as st
from cookies_helper import get_cookies

def restore_login():
    cookies = get_cookies()

    if not cookies:
        return

    if cookies.get("logged_in") == "true":
        st.session_state["logged_in"] = True
        st.session_state["username"] = cookies.get("username")
        st.session_state["user_id"] = cookies.get("user_id")