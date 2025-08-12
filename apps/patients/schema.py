from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class PatientSchema(BaseModel):
    """Schema for patient creation/update."""
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    organization: Optional[int] = None
    created_by: Optional[int] = None
    status: str = "active"


class PatientListSchema(BaseModel):
    """Schema for patient list response."""
    id: int
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: str 