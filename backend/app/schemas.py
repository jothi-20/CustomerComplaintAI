from pydantic import BaseModel
from typing import Optional

class ComplaintCreate(BaseModel):
    title: str
    description: str

class ComplaintStatusUpdate(BaseModel):
    status: str

class ComplaintFollowUp(BaseModel):
    remark: str