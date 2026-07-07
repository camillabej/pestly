import streamlit as st

@st.dialog("Konfirmasi Logout")
def konfirmasi_logout():
    st.write("Apakah Anda yakin ingin keluar dari akun?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚪 Ya, Logout", use_container_width=True):
            st.switch_page("pages/logout.py")

    with col2:
        if st.button("❌ Batal", use_container_width=True):
            st.rerun()