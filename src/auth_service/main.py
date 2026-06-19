from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
from models import UserRegister, UserLogin, TokenResponse
from security import hash_password, verify_password, create_access_token, decode_token
from database import get_user, create_user, user_exists

def get_allowed_origins():
    origins = os.environ.get(
        "FRONTEND_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"
    )
    return [origin.strip() for origin in origins.split(",") if origin.strip()]

app = FastAPI(
    title="SecureVault Bank - Auth Service",
    description="JWT RS256 Authentication with bcrypt and Redis rate limiting",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_methods=["*"],
    allow_headers=["*"]
)

try:
    r = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)
    r.ping()
    REDIS_AVAILABLE = True
except:
    REDIS_AVAILABLE = False

security = HTTPBearer()

def rate_limit_check(ip: str):
    if not REDIS_AVAILABLE:
        return
    key = f"login_attempts:{ip}"
    attempts = r.get(key)
    if attempts and int(attempts) >= 5:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again in 60 seconds.")

def record_failed_attempt(ip: str):
    if not REDIS_AVAILABLE:
        return
    key = f"login_attempts:{ip}"
    r.incr(key)
    r.expire(key, 60)

def clear_attempts(ip: str):
    if not REDIS_AVAILABLE:
        return
    r.delete(f"login_attempts:{ip}")

@app.get("/health")
def health():
    return {"status": "healthy", "service": "auth-service", "redis": REDIS_AVAILABLE}

@app.post("/auth/register", status_code=201)
def register(user: UserRegister):
    if user_exists(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    created = create_user(user.username, hashed, user.role)
    return {"message": "User registered successfully", "username": created["username"], "role": created["role"]}

@app.post("/auth/login", response_model=TokenResponse)
def login(user: UserLogin, request: Request):
    client_ip = request.client.host
    rate_limit_check(client_ip)
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        record_failed_attempt(client_ip)
        raise HTTPException(status_code=401, detail="Invalid username or password")
    clear_attempts(client_ip)
    token = create_access_token({"sub": user.username, "role": db_user["role"]})
    return TokenResponse(access_token=token, role=db_user["role"])

@app.get("/auth/verify")
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"username": payload.get("sub"), "role": payload.get("role"), "valid": True}

@app.post("/auth/logout")
def logout():
    return {"message": "Logged out successfully"}
