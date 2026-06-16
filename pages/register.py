
import streamlit as st
import auth
from supabase_client import supabase

st.set_page_config(
    page_title="Pestly - Register",
    page_icon="🫛",
    layout="wide"
)

# ==========================
# SEMBUNYIKAN SIDEBAR
# ==========================
st.markdown("""
<style>
section[data-testid="stSidebar"]{
    display:none;
}
[data-testid="stSidebarNav"]{
    display:none;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# LOAD CSS
# ==========================
with open("styles/register.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================
# BUTTON KEMBALI
# ==========================
if st.button("⬅️ Kembali"):
    st.switch_page("main.py")

# ==========================
# REGISTER PAGE
# ==========================
col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.markdown("""
    <div class="register-header">
        <div class="register-title">Register</div>
        <div class="register-subtitle">
            Buat akun untuk menggunakan sistem deteksi hama daun buncis
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form"):

        nama = st.text_input("Nama Lengkap")

        username = st.text_input("Username")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        konfirmasi = st.text_input(
            "Konfirmasi Password",
            type="password"
        )

        submit = st.form_submit_button(
            "📝 Daftar",
            use_container_width=True
        )
    if submit:

        if not nama or not username or not email or not password:
            st.error("Semua field wajib diisi!")

        elif password != konfirmasi:
            st.error("Password tidak sama!")

        else:

            try:

                cek_user = (
                    supabase.table("profiles")
                    .select("id")
                    .eq("username", username)
                    .execute()
                )

                if cek_user.data:
                    st.error("Username sudah digunakan!")
                    st.stop()
                    

                cek_user = (
                    supabase.table("profiles")
                    .select("id")
                    .eq("username", username)
                    .execute()
                )

                if cek_user.data:
                    st.error("Username sudah digunakan!")
                    st.stop()

                # BUAT USER DI SUPABASE AUTH
                auth_response = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                st.write("AUTH RESPONSE:", auth_response)
                user_id = auth_response.user.id

                # SIMPAN PROFILE
                supabase.table("profiles").insert({
                    "user_id": user_id,
                    "nama": nama,
                    "username": username,
                    "email": email
                }).execute()

                st.success(
                    "Registrasi berhasil! Silakan login."
                )

            except Exception as e:
                st.exception(e)


    st.markdown("<br>", unsafe_allow_html=True)
        
    st.page_link(
    "pages/login.py",
    label="Sudah punya akun?",
    icon=None
    )
