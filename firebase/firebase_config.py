import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase/montaj-7ad7d-firebase-adminsdk-fbsvc-1ae50963aa.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()
