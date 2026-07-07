import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Reset Password",
    page_icon="🔒",
    layout="centered"
)

st.markdown("""
<style>
section[data-testid="stSidebar"]{display:none;}
[data-testid="stSidebarNav"]{display:none;}
</style>
""", unsafe_allow_html=True)

st.title("🔒 Reset Password")

st.write("Masukkan password baru Anda.")

password = st.text_input(
    "Password Baru",
    type="password"
)

konfirmasi = st.text_input(
    "Konfirmasi Password Baru",
    type="password"
)

if st.button("💾 Simpan Password Baru", use_container_width=True):

    if not password or not konfirmasi:
        st.warning("Semua kolom harus diisi.")

    elif password != konfirmasi:
        st.error("Konfirmasi password tidak sesuai.")

    else:
        try:
            supabase.auth.update_user(
                {
                    "password": password
                }
            )

            st.success("✅ Password berhasil diperbarui.")

            if st.button("⬅️ Kembali ke Login"):
                st.switch_page("pages/login.py")

        except Exception as e:
            st.error("❌ Gagal mengubah password.")
            st.caption(str(e))