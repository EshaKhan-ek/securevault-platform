import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "auth.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL,
            balance REAL DEFAULT 1000.0
        )
    """)
    conn.commit()
    from security import hash_password
    existing = conn.execute("SELECT * FROM users WHERE username = 'admin'").fetchone()
    if not existing:
        conn.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
            ("admin", hash_password("Admin@1234"), "admin", 99999.0))
        conn.commit()
    conn.close()

def get_user(username: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(username: str, hashed_password: str, role: str):
    conn = get_connection()
    conn.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
        (username, hashed_password, role, 1000.0))
    conn.commit()
    conn.close()
    return {"username": username, "hashed_password": hashed_password, "role": role, "balance": 1000.0}

def user_exists(username: str) -> bool:
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row is not None

init_db()
