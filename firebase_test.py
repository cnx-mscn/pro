from firebase.firebase_config import init_firebase

# Firebase'e bağlan
db = init_firebase()

# Test verisi gönder
veri = {
    "mesaj": "Firebase bağlantısı başarılı 🎉",
    "durum": "test"
}

# Firestore'a veri ekle
db.collection("test_baglantisi").add(veri)

print("✅ Firebase Firestore'a veri gönderildi.")
