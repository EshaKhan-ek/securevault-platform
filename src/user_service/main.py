from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_current_user, require_admin
from database import get_user, create_user, get_all_users, init_db

app = FastAPI(
    title="SecureVault Bank - User Service",
    description="User management with RBAC - customer and admin roles",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()

@app.get("/health")
def health():
    return {"status": "healthy", "service": "user-service"}

@app.get("/users/me")
def get_my_profile(current_user: dict = Depends(get_current_user)):
    user = get_user(current_user["username"])
    if not user:
        return {"username": current_user["username"], "role": current_user["role"], "balance": 1000.0}
    return user

@app.get("/users/all")
def get_all_users_route(current_user: dict = Depends(require_admin)):
    users = get_all_users()
    return {"users": users, "total": len(users)}

@app.get("/users/{username}")
def get_user_by_username(username: str, current_user: dict = Depends(require_admin)):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/register-profile")
def register_profile(username: str, role: str, current_user: dict = Depends(get_current_user)):
    create_user(username, role)
    return {"message": "Profile created", "username": username}
