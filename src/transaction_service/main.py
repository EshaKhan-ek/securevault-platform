from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_current_user, require_admin
from models import TransactionCreate
from datetime import datetime
import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "transaction.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS balances (
            username TEXT PRIMARY KEY,
            balance REAL DEFAULT 1000.0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_username TEXT,
            to_username TEXT,
            amount REAL,
            description TEXT,
            status TEXT DEFAULT 'completed',
            timestamp TEXT
        )
    """)
    for username, bal in [("admin", 99999.0), ("esha", 1000.0)]:
        conn.execute("INSERT OR IGNORE INTO balances VALUES (?, ?)", (username, bal))
    conn.commit()
    conn.close()

def get_balance_db(username: str) -> float:
    conn = get_connection()
    row = conn.execute("SELECT balance FROM balances WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row:
        return row["balance"]
    set_balance_db(username, 1000.0)
    return 1000.0

def set_balance_db(username: str, amount: float):
    conn = get_connection()
    conn.execute("INSERT OR REPLACE INTO balances VALUES (?, ?)", (username, amount))
    conn.commit()
    conn.close()

def add_transaction_db(from_username, to_username, amount, description):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO transactions (from_username, to_username, amount, description, status, timestamp) VALUES (?, ?, ?, ?, 'completed', ?)",
        (from_username, to_username, amount, description, datetime.utcnow().isoformat())
    )
    conn.commit()
    tx_id = cursor.lastrowid
    conn.close()
    return tx_id

def get_user_transactions(username: str):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE from_username = ? OR to_username = ?",
        (username, username)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_transactions_db():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return [dict(r) for r in rows]

app = FastAPI(
    title="SecureVault Bank - Transaction Service",
    description="Secure money transfers with input validation and ABAC",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "transaction-service"}

@app.post("/transactions/send", status_code=201)
def send_money(tx: TransactionCreate, current_user: dict = Depends(get_current_user)):
    sender = current_user["username"]
    if tx.to_username == sender:
        raise HTTPException(status_code=400, detail="Cannot send money to yourself")
    if tx.amount <= 0 or tx.amount > 100000:
        raise HTTPException(status_code=400, detail="Amount must be between 0 and 100,000")
    sender_balance = get_balance_db(sender)
    if sender_balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    set_balance_db(sender, round(sender_balance - tx.amount, 2))
    set_balance_db(tx.to_username, round(get_balance_db(tx.to_username) + tx.amount, 2))
    tx_id = add_transaction_db(sender, tx.to_username, tx.amount, tx.description)
    return {"message": "Transaction successful", "transaction_id": tx_id, "new_balance": get_balance_db(sender)}

@app.get("/transactions/history")
def my_history(current_user: dict = Depends(get_current_user)):
    txs = get_user_transactions(current_user["username"])
    return {"transactions": txs, "count": len(txs)}

@app.get("/transactions/all")
def all_transactions(current_user: dict = Depends(require_admin)):
    txs = get_all_transactions_db()
    return {"transactions": txs, "count": len(txs)}

@app.get("/transactions/balance")
def get_balance_route(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    return {"username": username, "balance": get_balance_db(username)}
