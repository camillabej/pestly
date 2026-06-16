import streamlit as st
from supabase_client import supabase

def restore_login():
    try:
        session = supabase.auth.get_session()

        st.write("SESSION =", session)

        if session and session.session:
            user = session.session.user

            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.session_state["user_id"] = user.id
            st.session_state["email"] = user.email

    except Exception as e:
        st.write("ERROR =", e)