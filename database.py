import uuid
import streamlit as st
from datetime import datetime
from supabase_client import supabase


def get_db():
    return supabase


def init_db():
    pass


def simpan_riwayat(tanggal, image_bytes, deteksi_list):

    user_id = st.session_state.get("user_id")

    if not user_id:
        return False

    db = get_db()

    # Nama file unik
    filename = f"{uuid.uuid4()}.jpg"
    
    # Path lengkap file
    filepath = f"{folder}/{filename}"
    
    # Folder berdasarkan tanggal
    folder = datetime.now().strftime("%Y-%m-%d")

    # Upload ke bucket storage
    try:
        db.storage.from_("hasil-deteksi").upload(
            filename,
            image_bytes,
            {"content-type": "image/jpeg"}
        )
    except Exception as e:
        st.error(f"Gagal upload gambar: {e}")
        return False   

    # Ambil URL publik
    image_url = db.storage.from_("hasil-deteksi").get_public_url(filepath)

    # Simpan ke tabel riwayat
    try:
        db.table("riwayat").insert({
            "user_id": user_id,
            "tanggal": tanggal,
            "image_url": image_url,
            "deteksi": deteksi_list
        }).execute()
    except Exception as e:
        st.error(f"Gagal menyimpan riwayat: {e}")
        return False



def ambil_riwayat():
    user_id = st.session_state.get("user_id")

    if not user_id:
        return []

    db = get_db()

    response = (
        db.table("riwayat")
        .select("*")
        .eq("user_id", user_id)
        .order("id", desc=True)
        .execute()
    )

    return response.data if response.data else []


def hapus_riwayat(id):
    db = get_db()

    db.table("riwayat") \
        .delete() \
        .eq("id", id) \
        .execute()