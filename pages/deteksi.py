import streamlit as st
import base64
import io
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
from database import init_db, simpan_riwayat
from supabase_client import supabase
from auth import restore_login

st.set_page_config(
    page_title="Deteksi Hama - pestly",
    page_icon="🫛",
    layout="wide"
)

restore_login()

# Login Google
if st.user.is_logged_in:
    st.session_state["logged_in"] = True

init_db()

# ==========================
# LOAD CSS
# ==========================
def load_css():
    with open("styles/deteksi.css", encoding="utf-8") as f:
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
# PROTEKSI HALAMAN
# ==========================
if not st.session_state.get("logged_in") and not st.user.is_logged_in:
    st.switch_page("pages/login.py")
    st.stop()

# ==========================
# HEADER
# ==========================
col1, col2 = st.columns([8, 1])
with col1:
    st.title("📸 Deteksi Hama")
with col2:
    if st.user.is_logged_in:
        if st.button("🚪 Logout"):
            st.logout()
            st.switch_page("main.py")
    elif st.session_state.get("logged_in", False):
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.switch_page("main.py")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================
# LOAD MODEL (cached)
# ==========================
@st.cache_resource
def load_model():
    return YOLO("model/best.pt")

model = load_model()

LABEL_MAP = {
    "belalang": "Belalang",
    "ulat": "Ulat",
}

ICON_MAP = {
    "Belalang": "🦗",
    "Ulat": "🐛",
    "Sehat": "🌿"
}

SEVERITY_DESC = {
    "tinggi": "Segera lakukan penanganan",
    "sedang": "Perlu dipantau",
    "rendah": "Tidak terlalu mengkhawatirkan",
}

def get_severity(conf):
    if conf >= 0.7:
        return "Tinggi", "tinggi"
    elif conf >= 0.4:
        return "Sedang", "sedang"
    else:
        return "Rendah", "rendah"

# ==========================
# UPLOAD GAMBAR
# ==========================
st.markdown("""
<div class="upload-card">
<div class="feature-icon">📷</div>
<div class="feature-title">Upload Gambar Daun</div>
<div class="feature-desc">
Upload gambar daun buncis muda untuk mendeteksi hama belalang dan ulat menggunakan model <span class="highlight">YOLOv8</span>.
</div>
</div>
""", unsafe_allow_html=True)

# ==========================
# PILIH SUMBER GAMBAR
# ==========================
if "source_mode" not in st.session_state:
    st.session_state["source_mode"] = None

col_a, col_b = st.columns(2)
with col_a:
    if st.button("📁 Upload Gambar", use_container_width=True, type="primary" if st.session_state["source_mode"] == "upload" else "secondary"):
        st.session_state["source_mode"] = "upload"
with col_b:
    if st.button("📷 Buka Kamera", use_container_width=True, type="primary" if st.session_state["source_mode"] == "camera" else "secondary"):
        st.session_state["source_mode"] = "camera"

uploaded_file = None

if st.session_state["source_mode"] == "upload":
    uploaded_file = st.file_uploader(
        "Pilih gambar (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
elif st.session_state["source_mode"] == "camera":
    uploaded_file = st.camera_input("Ambil foto daun buncis")

st.markdown("<br>", unsafe_allow_html=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    # Preview gambar input
    buf_prev = io.BytesIO()
    fmt = Image.open(uploaded_file).format or "JPEG"
    if fmt not in ["JPEG", "PNG", "WEBP"]:
        fmt = "JPEG"
    image.save(buf_prev, format=fmt)
    img_b64 = base64.b64encode(buf_prev.getvalue()).decode()
    mime = "image/jpeg" if fmt == "JPEG" else f"image/{fmt.lower()}"

    st.markdown('<div class="result-title">📥 Gambar Input</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="preview-container">
        <img src="data:{mime};base64,{img_b64}" class="preview-image">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    mulai = st.button("🔍 Mulai Deteksi", type="primary", use_container_width=True)

    if mulai:
        col_img, col_result = st.columns(2)

        with col_img:
            st.markdown('<div class="result-title">📥 Gambar Input</div>', unsafe_allow_html=True)
            st.image(image, use_container_width=True)

        # ==========================
        # JALANKAN DETEKSI
        # ==========================
        with st.spinner("🔍 Mendeteksi hama..."):
            results = model.predict(image, conf=0.40, iou=0.35, agnostic_nms=True, verbose=False)
            result = results[0]
            result_img = result.plot()
            result_img = Image.fromarray(result_img[:, :, ::-1])

        with col_result:
            st.markdown('<div class="result-title">🎯 Hasil Deteksi</div>', unsafe_allow_html=True)
            st.image(result_img, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================
        # DAFTAR DETEKSI
        # ==========================
        boxes = result.boxes
        deteksi_list = []

        if boxes is not None and len(boxes) > 0:
            st.markdown('<div class="result-title">📋 Detail Deteksi</div>', unsafe_allow_html=True)

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label_raw = model.names[cls_id]
                label = LABEL_MAP.get(label_raw.lower(), label_raw.capitalize())
                severity_label, severity_class = get_severity(conf)

                deteksi_list.append({
                    "label": label,
                    "conf": conf,
                    "severity_label": severity_label,
                    "severity_class": severity_class,
                })

            items_html = ""
            for d in deteksi_list:
                icon = ICON_MAP.get(d["label"], "🌿")
                desc = SEVERITY_DESC.get(d["severity_class"], "")
                items_html += f"""
<div class="riwayat-item severity-border-{d['severity_class']}">
    <div class="riwayat-icon">{icon}</div>
    <div class="riwayat-info">
        <div class="riwayat-name">{d['label']}</div>
        <div class="riwayat-percent">Tingkat keyakinan: {d['conf']*100:.1f}%</div>
        <div class="confidence-bar">
            <div class="confidence-fill" style="width:{d['conf']*100:.1f}%; background:var(--sev-{d['severity_class']})"></div>
        </div>
        <div class="severity-desc">{desc}</div>
    </div>
    <span class="badge badge-{d['severity_class']}">{d['severity_label']}</span>
</div>"""

            st.markdown(f'<div class="detail-card">{items_html}</div>', unsafe_allow_html=True)

        else:
            deteksi_list = [{
                "label": "Sehat",
                "conf": 1.0,
                "severity_label": "Aman",
                "severity_class": "aman"
            }]
            st.success("🌿 Tidak ditemukan hama. Daun terdeteksi sehat.")

        # ==========================
        # SIMPAN KE DATABASE
        # ==========================
        image_hash = hash(uploaded_file.getvalue())

        if st.session_state.get("last_saved_hash") != image_hash:
            buf = io.BytesIO()
            result_small = result_img.copy()
            result_small.thumbnail((640, 640))
            result_small.save(buf, format="JPEG", quality=75)

            simpan_riwayat(
                tanggal=datetime.now().strftime("%d-%m-%Y %H:%M"),
                image_bytes=buf.getvalue(),
                deteksi_list=deteksi_list,
            )

            st.session_state["last_saved_hash"] = image_hash
            st.success("✅ Hasil deteksi otomatis disimpan ke riwayat!")

        else:
            st.info("ℹ️ Hasil deteksi ini sudah tersimpan di riwayat.")

else:
    st.markdown("""
    <div class="empty-result">
    📤 Silakan pilih Upload Gambar atau Buka Kamera untuk memulai deteksi.
    </div>
    """, unsafe_allow_html=True)