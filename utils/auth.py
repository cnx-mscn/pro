
import json
import os

USERS_FILE = "data/kullanicilar.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def register_user(username, password, role):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password, "role": role}
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    return True

def login_user(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None
