import streamlit as st
import io
from PIL import Image
from database import ambil_riwayat, hapus_riwayat
from auth import restore_login



st.set_page_config(
    page_title="Riwayat Deteksi - Pestly",
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
    with open("styles/riwayat.css", encoding="utf-8") as f:
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
col1, col2 = st.columns([8, 1])
with col1:
    st.title("📋 Riwayat Deteksi")
with col2:
    if st.session_state.get("logged_in", False):
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.switch_page("main.py")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# AMBIL DATA RIWAYAT
# ==========================
riwayat = ambil_riwayat()

# ==========================
# STATISTIK
# ==========================
total = len(riwayat)
total_sehat = sum(
    1 for r in riwayat for d in r["deteksi"] if d["label"] == "Sehat"
)
total_belalang = sum(
    1 for r in riwayat for d in r["deteksi"] if d["label"] == "Belalang"
)
total_ulat = sum(
    1 for r in riwayat for d in r["deteksi"] if d["label"] == "Ulat"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Total Deteksi</div>
        <div class="stat-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Sehat</div>
        <div class="stat-value">{total_sehat}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Belalang</div>
        <div class="stat-value">{total_belalang}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Ulat</div>
        <div class="stat-value">{total_ulat}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# FILTER
# ==========================
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    filter_hama = st.selectbox(
        "Filter jenis hama",
        ["Semua Hama", "Sehat", "Belalang", "Ulat"],
        label_visibility="collapsed"
    )

with col_filter2:
    filter_tingkat = st.selectbox(
        "Filter tingkat",
        ["Semua Tingkat", "Aman", "Tinggi", "Sedang", "Rendah"],
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# DAFTAR RIWAYAT
# ==========================
import base64

import base64

def get_icon_base64():
    with open("assets/daun.jpg", "rb") as f:
        return base64.b64encode(f.read()).decode()

if not riwayat:
    st.markdown("""
    <div class="empty-result">
    📭 Belum ada riwayat deteksi. Silakan lakukan deteksi terlebih dahulu.
    </div>
    """, unsafe_allow_html=True)
else:
    SEVERITY_DESC = {
        "tinggi": "Segera lakukan penanganan",
        "sedang": "Perlu dipantau",
        "rendah": "Tidak terlalu mengkhawatirkan",
    }

    severity_order = {"tinggi": 3, "sedang": 2, "rendah": 1}
    badge_color_map = {
        "tinggi": "#ef4444",
        "sedang": "#facc15",
        "rendah": "#22c55e",
    }

    # Filter dulu semua riwayat
    riwayat_filtered = []
    for r in riwayat:
        deteksi_tampil = [
            d for d in r["deteksi"]
            if (filter_hama == "Semua Hama" or d["label"] == filter_hama)
            and (filter_tingkat == "Semua Tingkat" or d["severity_label"] == filter_tingkat)
        ]
        if deteksi_tampil:
            riwayat_filtered.append((r, deteksi_tampil))

    if not riwayat_filtered:
        st.markdown("""
        <div class="empty-result">
        🔍 Tidak ada riwayat yang sesuai filter.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Tampilkan 2 card per baris
        for row_start in range(0, len(riwayat_filtered), 2):
            cols = st.columns(2)
            for col_idx, (r, deteksi_tampil) in enumerate(riwayat_filtered[row_start:row_start+2]):
                idx = riwayat.index(r)
                hama_utama = deteksi_tampil[0]
                icon_b64 = get_icon_base64()
                nama_list = ", ".join(d["label"] for d in deteksi_tampil)
                conf_avg = sum(d["conf"] for d in deteksi_tampil) / len(deteksi_tampil)
                hama_tertinggi = max(deteksi_tampil, key=lambda d: severity_order.get(d["severity_class"], 0))
                badge_color = badge_color_map.get(hama_tertinggi["severity_class"], "#9ca3af")

                with cols[col_idx]:
                    st.markdown(f"""
<div class="history-card">
    <div class="history-card-top">
        <img src="data:image/png;base64,{icon_b64}" class="history-card-img">
        <div class="history-card-right">
            <div class="history-card-name">{nama_list}</div>
            <div class="history-card-conf">{conf_avg*100:.1f}%</div>
        </div>
    </div>
    <div class="history-card-meta">🗓️ {r['tanggal']}</div>
    <div class="history-card-meta">📊 Tingkat : <span style="background:rgba(239,68,68,.15);color:{badge_color};padding:2px 10px;border-radius:999px;font-weight:700;">{hama_tertinggi["severity_label"]}</span></div>
</div>
                    """, unsafe_allow_html=True)

                    if st.button("👁️ Lihat Detail", key=f"detail_{r['id']}", use_container_width=True):
                        st.session_state["detail_riwayat"] = r
                        st.switch_page("pages/detail.py")

                    if st.session_state.get(f"show_detail_{r['id']}", False):
                        if r.get("image_url"):
                            st.image(
                                r["image_url"],
                                use_container_width=True
                            )

                        items_html = ""
                        for d in deteksi_tampil:
                            desc = SEVERITY_DESC.get(d["severity_class"], "")
                            icon_d = get_icon_base64(d["label"])
                            items_html += f"""
<div class="riwayat-item severity-border-{d['severity_class']}">
    <div class="riwayat-icon"><img src="data:image/png;base64,{icon_d}" width="35" height="35" style="object-fit:contain;"></div>
    <div class="riwayat-info">
        <div class="riwayat-name">{d['label']}</div>
        <div class="riwayat-percent">Tingkat keyakinan: {d['conf']*100:.1f}%</div>
        <div class="confidence-bar"><div class="confidence-fill" style="width:{d['conf']*100:.1f}%; background:var(--sev-{d['severity_class']})"></div></div>
        <div class="severity-desc">{desc}</div>
    </div>
    <span class="badge badge-{d['severity_class']}">{d['severity_label']}</span>
</div>
                            """
                        st.markdown(f'<div class="detail-card">{items_html}</div>', unsafe_allow_html=True)

                        if st.button("🗑️ Hapus", key=f"hapus_{r['id']}", use_container_width=True):
                            hapus_riwayat(r["id"])
                            st.rerun()