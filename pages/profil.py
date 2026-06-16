import streamlit as st
from auth import restore_login

st.set_page_config(
    page_title="Profil - Pestly",
    page_icon="🫛",
    layout="wide"
)

restore_login()

# ==========================
# PROTEKSI HALAMAN
# ==========================
if not st.session_state.get("logged_in"):
    st.switch_page("pages/login.py")
    st.stop()

# ==========================
# LOAD CSS
# ==========================
def load_css():
    with open("styles/profil.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">🫛</div>
    <div class="sidebar-title">Pestly</div>
    <div class="sidebar-subtitle">AI Pest Detection</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.page_link("pages/home.py", label="Dashboard", icon="🏠")
    st.page_link("pages/deteksi.py", label="Deteksi Hama", icon="📸")
    st.page_link("pages/riwayat.py", label="Riwayat Deteksi", icon="📋")
    st.page_link("pages/profil.py", label="Profil", icon="👤")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.page_link("pages/logout.py", label="Logout", icon="🚪")



# ==========================
# HEADER
# ==========================

st.title("👤 Profil")
st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# AMBIL DATA USER
# ==========================
nama = st.session_state.get("username", "User")
email = st.session_state.get("email", "Tidak tersedia")
foto = None

inisial = "".join([w[0].upper() for w in nama.split()[:2]]) if nama else "U"

# ==========================
# CARD PROFIL
# ==========================
if foto:
    avatar_html = f'<img src="{foto}" class="profile-avatar-img">'
else:
    avatar_html = f'<div class="profile-avatar">{inisial}</div>'

st.markdown(f"""
<div class="profile-card">
    <div class="profile-header">
        {avatar_html}
        <div>
            <div class="profile-name">{nama}</div>
            <div class="profile-email">📧 {email}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ==========================
# INFORMASI AKUN
# ==========================
st.markdown('<div class="result-title">⚙️ Informasi Akun</div>', unsafe_allow_html=True)

metode_login = "Supabase"

st.markdown(f"""
<div class="info-sub-card">
    <table class="profile-table">
        <tr>
            <td>Nama</td>
            <td>{nama}</td>
        </tr>
        <tr>
            <td>Email</td>
            <td>{email}</td>
        </tr>
        <tr>
            <td>Metode Login</td>
            <td>{metode_login}</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# AKSI AKUN
# ==========================

if st.button("🚪 Logout", use_container_width=True, key="logout_bottom"):
    st.session_state.clear()
    st.switch_page("main.py")