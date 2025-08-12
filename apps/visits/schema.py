from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VisitSchema(BaseModel):
    """Schema for visit creation/update."""
    patient: int
    doctor: int
    technician: Optional[int] = None
    organization: int
    scheduled_date: datetime
    actual_date: Optional[datetime] = None
    status: str = "scheduled"
    priority: str = "normal"
    symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None


class VisitListSchema(BaseModel):
    """Schema for visit list response."""
    id: int
    patient: int
    doctor: int
    scheduled_date: datetime
    status: str
    priority: str 