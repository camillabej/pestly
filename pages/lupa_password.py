import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Lupa Password",
    page_icon="🔑",
    layout="centered"
)

st.markdown("""
<style>
section[data-testid="stSidebar"]{ display:none; }
[data-testid="stSidebarNav"]{ display:none; }
</style>
""", unsafe_allow_html=True)

def load_css():
    with open("styles/login.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.title("🔑 Lupa Password")


st.write(
    "Masukkan email yang terdaftar. Kami akan mengirimkan tautan untuk mengatur ulang password."
)

email = st.text_input(
    "Email",
    placeholder="Masukkan email yang terdaftar"
)

if st.button("📩 Kirim Link Reset", use_container_width=True):

    if not email:
        st.warning("Silakan masukkan email.")
    else:
        try:
            supabase.auth.reset_password_email(
                email,
                redirect_to="https://pestly-deteksi-hama.streamlit.app/reset_password")

            st.success(
                "✅ Link reset password berhasil dikirim. Silakan cek email Anda."
            )

        except Exception:
            st.error("❌ Gagal mengirim link reset password.")

if st.button("⬅️ Kembali ke Login", use_container_width=True):
    st.switch_page("pages/login.py")