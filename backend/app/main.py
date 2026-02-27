# app/main.py
from fastapi import FastAPI
from app.routes import complaints
from app.database import init_db

app = FastAPI(title="ComplaintAI Backend")

# Initialize SQLite DB
init_db()

# Include routes
app.include_router(complaints.router)