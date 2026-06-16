import streamlit as st
from supabase_client import supabase

def restore_login():
    try:
        session = supabase.auth.get_session()

        if session and session.session:
            user = session.session.user

            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.session_state["user_id"] = user.id
            st.session_state["email"] = user.email

            if "username" not in st.session_state:
                st.session_state["username"] = (
                    user.user_metadata.get("full_name")
                    or user.user_metadata.get("name")
                    or user.email
                )

    except Exception:
        pass