import sqlite3
from pathlib import Path

DB_PATH = Path("data/complaints.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE complaints ADD COLUMN tags TEXT")
    print("Column 'tags' added successfully.")
except sqlite3.OperationalError as e:
    print("Column probably already exists:", e)

conn.commit()
conn.close()