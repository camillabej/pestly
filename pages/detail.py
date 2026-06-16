
import streamlit as st
from database import hapus_riwayat
from auth import restore_login


st.set_page_config(
    page_title="Detail Deteksi - Pestly",
    page_icon="🫛",
    layout="wide"
)
restore_login()
# ==========================
# LOAD CSS
# ==========================
def load_css():
    with open("styles/detail.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
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

    st.page_link(
        "pages/home.py",
        label="Dashboard",
        icon="🏠"
    )

    st.page_link(
        "pages/deteksi.py",
        label="Deteksi Hama",
        icon="📸"
    )

    st.page_link(
        "pages/riwayat.py",
        label="Riwayat Deteksi",
        icon="📋"
    )

    st.page_link(
        "pages/profil.py",
        label="Profil",
        icon="👤"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.page_link(
        "pages/logout.py",
        label="Logout",
        icon="🚪"
    )

# ==========================
# PROTEKSI HALAMAN
# ==========================
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()

# ==========================
# AMBIL DATA DETAIL
# ==========================
r = st.session_state.get("detail_riwayat")

if not r:
    st.switch_page("pages/riwayat.py")

# ==========================
# HEADER
# ==========================
st.title("📋 Detail Deteksi")

st.markdown(
    f"🗓️ {r['tanggal']}"
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# GAMBAR HASIL DETEKSI
# ==========================
if r.get("image_url"):

    st.markdown(
        f"""
        <div class="detail-image-wrapper">
            <img
                src="{r['image_url']}"
                class="detail-image"
            >
        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================
# DETAIL HAMA
# ==========================

SEVERITY_DESC = {
    "tinggi": "Segera lakukan penanganan",
    "sedang": "Perlu dipantau",
    "rendah": "Tidak terlalu mengkhawatirkan",
    "aman": "Tanaman dalam kondisi baik"
}

items_html = ""

for d in r["deteksi"]:

    label = d["label"]

    if label.lower() == "belalang":
        icon = "🦗"
    elif label.lower() == "ulat":
        icon = "🐛"
    else:
        icon = "🌿"

    desc = SEVERITY_DESC.get(
        d["severity_class"],
        ""
    )

    items_html += f"""
<div class="riwayat-item severity-border-{d['severity_class']}">

<div class="riwayat-icon">{icon}</div>
<div class="riwayat-info"> <div class="riwayat-name">{label}</div>
<div class="riwayat-percent">Tingkat keyakinan:
                {d['conf']*100:.1f}%
</div>

<div class="confidence-bar"><div
class="confidence-fill"style="width:{d['conf']*100:.1f}%;background:var(--sev-{d['severity_class']})">
</div></div>
<div class="severity-desc">{desc}</div>
</div>
<span class="badge badge-{d['severity_class']}">
            {d['severity_label']}
</span>

</div>
    """

st.markdown(
    f"""
<div class="detail-card">
        {items_html}
</div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# TOMBOL AKSI
# ==========================
col1, col2 = st.columns(2)

with col1:

    if st.button(
        "⬅️ Kembali",
        use_container_width=True
    ):
        st.switch_page(
            "pages/riwayat.py"
        )

with col2:

    if st.button(
        "🗑️ Hapus",
        use_container_width=True
    ):
        hapus_riwayat(r["id"])

        st.switch_page(
            "pages/riwayat.py"
        )

