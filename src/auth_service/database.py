from security import hash_password

# In-memory database (simulates a real DB for demo)
fake_db = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("Admin@1234"),
        "role": "admin",
        "balance": 99999.0
    }
}

def get_user(username: str):
    return fake_db.get(username)

def create_user(username: str, hashed_password: str, role: str):
    fake_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "role": role,
        "balance": 1000.0
    }
    return fake_db[username]

def user_exists(username: str) -> bool:
    return username in fake_db
