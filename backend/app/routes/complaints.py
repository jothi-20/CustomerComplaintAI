# app/routes/complaints.py

from fastapi import APIRouter, HTTPException
from app.schemas import ComplaintCreate, ComplaintStatusUpdate, ComplaintFollowUp
from app import crud

router = APIRouter()

@router.post("/complaints")
def create_complaint_endpoint(complaint: ComplaintCreate):
    return crud.create_complaint(complaint)

@router.get("/complaints")
def get_complaints():
    return crud.get_all_complaints()

@router.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: int):
    result = crud.get_complaint_by_id(complaint_id)
    if not result:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return result

@router.put("/complaints/{complaint_id}/status")
def update_status(complaint_id: int, status_update: ComplaintStatusUpdate):
    return crud.update_status(complaint_id, status_update.status)

@router.post("/complaints/{complaint_id}/followup")
def add_followup(complaint_id: int, followup: ComplaintFollowUp):
    return crud.add_followup(complaint_id, followup.remark)