import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "user.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            role TEXT NOT NULL,
            balance REAL DEFAULT 1000.0
        )
    """)
    for username, role, bal in [("admin", "admin", 99999.0), ("esha", "customer", 1000.0)]:
        conn.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (username, role, bal))
    conn.commit()
    conn.close()

def get_user(username: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(username: str, role: str, balance: float = 1000.0):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (username, role, balance))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]

init_db()
