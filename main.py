from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt
import sqlite3
import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# ---------------- CONFIG ----------------
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

# ---------------- APP ----------------
app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# ---------------- ARGON2 SETUP ----------------
ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64 MB
    parallelism=1
)

# ---------------- HOME ROUTE ----------------
@app.get("/")
def home():
    return {"message": "FastAPI server is running"}

# ---------------- DB UTILS ----------------
def get_user(username: str):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT username, password FROM users WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    conn.close()
    return user

# ---------------- PASSWORD VERIFY ----------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

# ---------------- LOGIN ENDPOINT ----------------
@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    user = get_user(username)

    if not user or not verify_password(password, user[1]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
    }