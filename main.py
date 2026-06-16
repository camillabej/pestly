import streamlit as st
from supabase_client import supabase

st.set_page_config(
    page_title="Pestly - Deteksi Hama Tanaman Daun Buncis Muda",
    page_icon="🫛",
    layout="wide"
)

st.write(supabase.auth.get_session())

query_params = st.query_params

if "code" in query_params:
    try:
        code = query_params["code"]

        response = supabase.auth.exchange_code_for_session({
            "auth_code": code
        })

        if response.user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = response.user
            st.session_state["user_id"] = response.user.id
            st.session_state["email"] = response.user.email

            st.switch_page("pages/home.py")

    except Exception as e:
        st.error(f"OAuth Error: {e}")
# Redirect ke Home jika sudah login
if st.session_state.get("logged_in"):
    st.switch_page("pages/home.py")
    
    
if not st.session_state.get("logged_in"):
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display:none;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================
# LOAD CSS
# ==========================
def load_css():
    with open("styles/style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# Header
col1, col2, col3 = st.columns([8, 1.5, 1.5])

with col1:
    st.markdown("## 🫛 Pestly")
    
with col2:
    if st.button("Login"):
        st.switch_page("pages/login.py")

with col3:
    if st.button("Register"):
        st.switch_page("pages/register.py")

st.divider()

# Hero Section
col1, col2 = st.columns([2,2])
with col1:

    st.markdown("""
    <div class="hero-section">

    <h1>
    Sistem Deteksi Hama Tanaman Daun Buncis
    </h1>

    <div class="hero-subtitle">
    Berbasis Deep Learning YOLOv8
    </div>

    <div class="hero-desc">
    Deteksi hama pada tanaman daun buncis secara cepat dan akurat
    menggunakan teknologi Computer Vision dan Deep Learning.
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 Mulai Sekarang"):
        st.switch_page("pages/login.py")
        
with col2:
    st.image("assets/buncis (2).png", use_container_width=True)


st.divider()


# Footer
st.caption("© 2026 Camilla")

