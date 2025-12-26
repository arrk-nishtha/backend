# Login Backend (FastAPI)

This project is a simple authentication backend built using FastAPI and SQLite.

## Files
- `main.py` – FastAPI application with login API
- `init_db.py` – Initializes the SQLite database and inserts users
- `users.db` – SQLite database storing user credentials (hashed)

## Features
- User authentication using FastAPI
- Password hashing with Argon2
- SQLite database for storage
- Login endpoint returns Authorization token

## Setup
Install dependencies:
```bash
pip install fastapi uvicorn argon2-cffi

Initialize database:  python init_db.py

Run server:
python -m uvicorn main:app --reload

Server runs at:
http://127.0.0.1:8000 

API Endpoint
POST /login
