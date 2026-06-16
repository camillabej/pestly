import supabase_client
import streamlit as st
from supabase_client import supabase
from auth import restore_login

st.set_page_config(
    page_title="Dashboard Pestly",
    page_icon="🫛",
    layout="wide"
)

restore_login()


if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")
    st.stop()

def load_css():
    with open("styles/home.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown('''
<style>
[data-testid="stSidebarNav"] { display: none; }
</style>
''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''
    <div class="sidebar-logo">🫛</div>
    <div class="sidebar-title">Pestly</div>
    <div class="sidebar-subtitle">AI Pest Detection</div>
    ''', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("pages/home.py", label="Dashboard", icon="🏠")
    st.page_link("pages/deteksi.py", label="Deteksi Hama", icon="📸")
    st.page_link("pages/riwayat.py", label="Riwayat Deteksi", icon="📋")
    st.page_link("pages/profil.py", label="Profil", icon="👤")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.page_link("pages/logout.py", label="Logout", icon="🚪")

col1, col2 = st.columns([8, 1])
with col1:
    st.title("🏠 Dashboard Pestly")
with col2:
    if st.session_state.get("logged_in", False):
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.switch_page("main.py")

nama = st.session_state.get("username", "User")

st.markdown(f'''
<div class="welcome-banner">
<h1>Selamat Datang, {nama}!</h1>
<p>Selamat datang di <b>Pestly</b> — Sistem Deteksi Hama Tanaman <span>Daun Buncis Muda</span>.</p>
<p>Deteksi hama belalang dan ulat menggunakan teknologi <span>Deep Learning YOLOv8</span> secara cepat dan akurat.</p>
</div>
''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown('''
        <div class="feature-icon">📷</div>
        <div class="feature-title">Deteksi Hama</div>
        <div class="feature-desc">Upload gambar daun buncis muda untuk mendeteksi hama menggunakan model Deep Learning YOLOv8.</div>
        ''', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Mulai Deteksi", key="deteksi", use_container_width=True):
            st.switch_page("pages/deteksi.py")

with col2:
    with st.container(border=True):
        st.markdown('''
        <div class="feature-icon">📋</div>
        <div class="feature-title">Riwayat Deteksi</div>
        <div class="feature-desc">Lihat seluruh hasil deteksi yang pernah dilakukan sebelumnya beserta informasi hama.</div>
        ''', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📖 Lihat Riwayat", key="riwayat", use_container_width=True):
            st.switch_page("pages/riwayat.py")
