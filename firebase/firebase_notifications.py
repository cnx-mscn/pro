
from firebase_config import init_firebase
import datetime

db = init_firebase()

def send_notification(message, to_role):
    notif = {
        "message": message,
        "to_role": to_role,
        "timestamp": datetime.datetime.now().isoformat()
    }
    db.collection("notifications").add(notif)

def get_notifications(role):
    docs = db.collection("notifications").order_by("timestamp", direction="DESCENDING").limit(10).stream()
    return [doc.to_dict() for doc in docs if doc.to_dict()["to_role"] == role]
