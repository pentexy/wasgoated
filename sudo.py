import json
import os
from config import OWNER_ID

SUDO_USERS_FILE = 'sudo_users.json'

if not os.path.exists(SUDO_USERS_FILE):
    with open(SUDO_USERS_FILE, 'w') as file:
        json.dump([OWNER_ID], file)  # Initialize with OWNER_ID as the first sudo user

def load_sudo_users():
    with open(SUDO_USERS_FILE, 'r') as file:
        return json.load(file)

def save_sudo_users(users):
    with open(SUDO_USERS_FILE, 'w') as file:
        json.dump(users, file)

def add_sudo(user_id):
    users = load_sudo_users()
    if user_id not in users:
        users.append(user_id)
        save_sudo_users(users)
        return True
    return False

def remove_sudo(user_id):
    users = load_sudo_users()
    if user_id in users:
        users.remove(user_id)
        save_sudo_users(users)
        return True
    return False

def is_sudo(user_id):
    users = load_sudo_users()
    return user_id in users
