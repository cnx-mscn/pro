
import streamlit as st
import json
from datetime import date
import uuid

from utils.auth import load_users, register_user, login_user
from utils.task_utils import load_tasks, save_tasks
from utils.geo_utils import get_coordinates
from utils.map_utils import create_map
from utils.pdf_utils import generate_pdf
from utils.ai_suggestion import öneri_üret
from utils.ai_route_map import rota_olustur
from utils.google_calendar import add_event_to_calendar

st.set_page_config(page_title="Montaj Yönetim Sistemi", layout="wide")

# === Giriş Sistemi ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user = None

users = load_users()

st.markdown("<h1>🔐 Montaj Yönetim Paneli</h1>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    secim = st.radio("İşlem seçin:", ["Giriş Yap", "Kayıt Ol"])
    if secim == "Giriş Yap":
        kullanici = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        if st.button("Giriş"):
            rol = login_user(kullanici, sifre)
            if rol:
                st.session_state.logged_in = True
                st.session_state.role = rol
                st.session_state.user = kullanici
                st.experimental_rerun()
            else:
                st.error("Geçersiz kullanıcı adı veya şifre.")
    else:
        yeni_kullanici = st.text_input("Yeni Kullanıcı Adı")
        yeni_sifre = st.text_input("Şifre", type="password")
        yeni_rol = st.selectbox("Rol", ["Yönetici", "İşçi"])
        if st.button("Kayıt Ol"):
            basarili = register_user(yeni_kullanici, yeni_sifre, yeni_rol)
            if basarili:
                st.success("Kayıt başarılı. Giriş yapabilirsiniz.")
            else:
                st.error("Bu kullanıcı adı zaten var.")
    st.stop()

# === Giriş yapıldıysa ===
st.sidebar.success(f"Giriş yapıldı: {st.session_state.user} ({st.session_state.role})")
tasks = load_tasks()

# === Yönetici Arayüzü ===
if st.session_state.role == "Yönetici":
    st.header("📋 Görev Atama")
    gorev_adi = st.text_input("Görev Adı")
    sehir = st.text_input("Şehir / Lokasyon")
    aciklama = st.text_area("Açıklama")
    atanan = st.text_input("Atanan (İşçi adı)")
    tarih = st.date_input("Tarih", date.today())

    if st.button("Görevi Ekle"):
        lat, lon = get_coordinates(sehir)
        task = {
            "id": str(uuid.uuid4()),
            "gorev_adi": gorev_adi,
            "sehir": sehir,
            "aciklama": aciklama,
            "atanan": atanan,
            "tarih": str(tarih),
            "lat": lat,
            "lon": lon,
            "durum": "beklemede",
            "foto": ""
        }
        tasks.append(task)
        save_tasks(tasks)
        st.success("Görev eklendi.")

    st.subheader("📍 Harita")
    from streamlit_folium import st_folium
    harita = create_map(tasks)
    st_folium(harita, height=500)

    st.subheader("📤 Görevleri PDF Olarak İndir")
    if st.button("PDF İndir"):
        pdf = generate_pdf(tasks)
        st.download_button("PDF'yi İndir", pdf, file_name="gorevler.pdf")

    st.subheader("📆 Google Takvime Ekle")
    if st.button("Google Calendar’a Aktar"):
        for t in tasks:
            if t["durum"] == "beklemede":
                add_event_to_calendar(
                    summary=t["gorev_adi"],
                    description=f"{t['aciklama']} - {t['sehir']}",
                    date=t["tarih"]
                )
        st.success("Tüm görevler takvime eklendi.")

    st.subheader("🤖 Yapay Zeka Görev Önerisi")
    if st.button("AI Görev Önerisi Al"):
        tamamlanan = [t for t in tasks if t["durum"] == "tamamlandı"]
        cevap = öneri_üret(tamamlanan)
        st.info(cevap)

    st.subheader("🧠 AI Rota Önerisi")
    if st.button("AI Rota Sıralaması Al"):
        cevap = rota_olustur(tasks)
        st.markdown(cevap)

# === İşçi Arayüzü ===
elif st.session_state.role == "İşçi":
    st.header("👷 Atanmış Görevleriniz")
    for i, task in enumerate(tasks):
        if task["atanan"] == st.session_state.user:
            st.markdown(f"**{task['tarih']} - {task['sehir']}**")
            st.text(task["aciklama"])
            if task["durum"] == "beklemede":
                foto = st.file_uploader(f"{task['gorev_adi']} için foto yükle", type=["jpg", "png"], key=f"foto{i}")
                if foto:
                    task["durum"] = "tamamlandı"
                    task["foto"] = foto.name
                    save_tasks(tasks)
                    st.success("Fotoğraf yüklendi. Görev tamamlandı.")
            else:
                st.success("✅ Bu görev tamamlandı.")

# === Firebase Test Butonu (isteğe bağlı)
with st.expander("🔥 Firebase Bağlantı Testi"):
    if st.button("🔌 Testi Başlat"):
        from firebase.firebase_config import init_firebase
        db = init_firebase()
        db.collection("test_baglantisi").add({"mesaj": "Streamlit üzerinden test 🎉"})
        st.success("✅ Firebase'e veri gönderildi.")
