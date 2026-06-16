import streamlit as st
from supabase_client import supabase


st.set_page_config(
    page_title="Pestly - Deteksi Hama Tanaman Daun Buncis Muda",
    page_icon="🫛",
    layout="wide"
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

if st.button("⬅️ Kembali"):
    st.switch_page("main.py")

def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("Login")
        st.markdown("<p style='text-align:center;color:#cbd5e1'>Masuk untuk menggunakan sistem deteksi hama daun buncis</p>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("🚀 Login", use_container_width=True):
            try:
                profile = (
                    supabase.table("profiles")
                    .select("*")
                    .eq("username", username)
                    .execute()
                )
                if not profile.data:
                    st.error("Username tidak ditemukan")
                    

                email = profile.data[0]["email"]
                auth = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                st.session_state["logged_in"] = True
                st.session_state["user"] = auth.user
                st.session_state["user_id"] = auth.user.id
                st.session_state["username"] = username
                st.session_state["access_token"] = auth.session.access_token
                st.session_state["refresh_token"] = auth.session.refresh_token

                #cookies = get_cookies()
                #cookies["logged_in"] = "true"
                #cookies["username"] = username
                #cookies["user_id"] = auth.user.id
                #cookies["access_token"] = auth.session.access_token
                #cookies["refresh_token"] = auth.session.refresh_token
                #cookies.save()

                st.success("Login berhasil")
                st.switch_page("pages/home.py")
            except Exception as e:
                    st.exception(e)

if st.button(
    "🔑 Login dengan Google",
    use_container_width=True
):
    response = supabase.auth.sign_in_with_oauth(
        {
            "provider": "google"
        }
    )

    st.markdown(
        f"""
        <meta http-equiv="refresh" content="0; url={response.url}">
        """,
        unsafe_allow_html=True
    )

login_page()
    



