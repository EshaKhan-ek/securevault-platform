from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_current_user, require_admin
from models import TransactionCreate
from datetime import datetime

app = FastAPI(
    title="SecureVault Bank - Transaction Service",
    description="Secure money transfers with input validation and ABAC",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

balances = {
    "admin": 99999.0,
    "esha":  1000.0
}
transactions = []
tx_counter = 1

@app.get("/health")
def health():
    return {"status": "healthy", "service": "transaction-service"}

@app.post("/transactions/send", status_code=201)
def send_money(tx: TransactionCreate, current_user: dict = Depends(get_current_user)):
    global tx_counter
    sender = current_user["username"]
    if tx.to_username == sender:
        raise HTTPException(status_code=400, detail="Cannot send money to yourself")
    if tx.amount <= 0 or tx.amount > 100000:
        raise HTTPException(status_code=400, detail="Amount must be between 0 and 100,000")
    sender_balance = balances.get(sender, 1000.0)
    if sender_balance < tx.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    balances[sender] = round(sender_balance - tx.amount, 2)
    balances[tx.to_username] = round(balances.get(tx.to_username, 1000.0) + tx.amount, 2)
    record = {
        "id": tx_counter, "from_username": sender, "to_username": tx.to_username,
        "amount": tx.amount, "description": tx.description,
        "status": "completed", "timestamp": datetime.utcnow().isoformat()
    }
    transactions.append(record)
    tx_counter += 1
    return {"message": "Transaction successful", "transaction_id": record["id"], "new_balance": balances[sender]}

@app.get("/transactions/history")
def my_history(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    my_txs = [t for t in transactions if t["from_username"] == username or t["to_username"] == username]
    return {"transactions": my_txs, "count": len(my_txs)}

@app.get("/transactions/all")
def all_transactions(current_user: dict = Depends(require_admin)):
    return {"transactions": transactions, "count": len(transactions)}

@app.get("/transactions/balance")
def get_balance(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    return {"username": username, "balance": balances.get(username, 1000.0)}
