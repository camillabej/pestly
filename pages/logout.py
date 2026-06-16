import streamlit as st
from supabase_client import supabase

st.set_page_config(page_title="Logout")

try:
    supabase.auth.sign_out()
except:
    pass

st.session_state.clear()

st.switch_page("main.py")