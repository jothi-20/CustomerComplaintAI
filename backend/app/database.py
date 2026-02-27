import sqlite3
from pathlib import Path

DB_PATH = Path("data/complaints.db")
DB_PATH.parent.mkdir(exist_ok=True)  # Ensure data folder exists

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Create complaints table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT,
        priority TEXT,
        status TEXT DEFAULT 'Draft',
        sla_date TEXT,
        follow_up TEXT,
        tags TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()