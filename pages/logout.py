import streamlit as st

st.set_page_config(page_title="Logout")

st.session_state.clear()

st.switch_page("main.py")