import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="pestly_",
    password=st.secrets["COOKIE_PASSWORD"],
)

if not cookies.ready():
    st.stop()


def get_cookies():
    return cookies