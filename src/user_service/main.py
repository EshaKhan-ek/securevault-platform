from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_current_user, require_admin

app = FastAPI(
    title="SecureVault Bank - User Service",
    description="User management with RBAC - customer and admin roles",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

users_db = {
    "admin": {"username": "admin", "role": "admin", "balance": 99999.0},
    "esha":  {"username": "esha",  "role": "customer", "balance": 1000.0}
}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "user-service"}

@app.get("/users/me")
def get_my_profile(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    user = users_db.get(username)
    if not user:
        return {"username": username, "role": current_user["role"], "balance": 1000.0}
    return user

@app.get("/users/all")
def get_all_users(current_user: dict = Depends(require_admin)):
    return {"users": list(users_db.values()), "total": len(users_db)}

@app.get("/users/{username}")
def get_user_by_username(username: str, current_user: dict = Depends(require_admin)):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/register-profile")
def register_profile(username: str, role: str, current_user: dict = Depends(get_current_user)):
    if username not in users_db:
        users_db[username] = {"username": username, "role": role, "balance": 1000.0}
    return {"message": "Profile created", "username": username}
