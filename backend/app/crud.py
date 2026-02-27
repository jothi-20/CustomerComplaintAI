# app/crud.py

from app.database import get_connection
from app.ai_engine import generate_case_note
from datetime import datetime, timedelta
from app.schemas import ComplaintCreate

def create_complaint(data: ComplaintCreate):
    conn = get_connection()
    cursor = conn.cursor()

    # Determine category and priority
    category, priority = "General", "Low"
    desc_lower = data.description.lower()
    if "login" in desc_lower or "password" in desc_lower:
        category, priority = "Authentication", "High"
    elif "error" in desc_lower or "failure" in desc_lower:
        category, priority = "System Error", "Medium"

    # SLA calculation
    if priority == "High":
        sla_date = datetime.utcnow() + timedelta(days=1)
    elif priority == "Medium":
        sla_date = datetime.utcnow() + timedelta(days=3)
    else:
        sla_date = datetime.utcnow() + timedelta(days=5)

    # Insert base complaint
    cursor.execute("""
        INSERT INTO complaints (title, description, category, priority, sla_date)
        VALUES (?, ?, ?, ?, ?)
    """, (data.title, data.description, category, priority, sla_date.isoformat()))
    complaint_id = cursor.lastrowid

    # Generate AI notes
    ai_note = generate_case_note(data.description)
    follow_up_str = str(ai_note)
    tags_str = ", ".join(ai_note.get("tags", []))

    cursor.execute("""
        UPDATE complaints
        SET follow_up = ?, tags = ?, updated_at = ?
        WHERE id = ?
    """, (follow_up_str, tags_str, datetime.utcnow().isoformat(), complaint_id))

    conn.commit()
    cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def get_all_complaints():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_complaint_by_id(complaint_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_status(complaint_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    updated_at = datetime.utcnow().isoformat()
    cursor.execute("""
        UPDATE complaints
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (status, updated_at, complaint_id))
    conn.commit()
    cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def add_followup(complaint_id: int, followup_text: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT follow_up FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    current_followup = row["follow_up"] if row and row["follow_up"] else ""
    updated_followup = current_followup + f"\n{datetime.utcnow().isoformat()}: {followup_text}"
    cursor.execute("""
        UPDATE complaints
        SET follow_up = ?, updated_at = ?
        WHERE id = ?
    """, (updated_followup, datetime.utcnow().isoformat(), complaint_id))
    conn.commit()
    cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)