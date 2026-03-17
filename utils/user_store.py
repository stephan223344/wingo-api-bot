import os

USERS_FILE = "users.txt"

def get_users() -> list[str]:
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as f:
        return f.read().splitlines()


def save_user(user_id: int):
    users = get_users()

    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")