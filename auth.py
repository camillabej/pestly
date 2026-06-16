import streamlit as st
from cookies_helper import get_cookies

def restore_login():

    if st.session_state.get("logged_in"):
        return

    cookies = get_cookies()

    if not cookies.ready():
        return

    if cookies.get("logged_in") == "true":

        st.session_state["logged_in"] = True
        st.session_state["username"] = cookies.get("username")
        st.session_state["user_id"] = cookies.get("user_id")
        st.session_state["access_token"] = cookies.get("access_token")
        st.session_state["refresh_token"] = cookies.get("refresh_token")