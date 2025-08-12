from pydantic import BaseModel, EmailStr
from typing import Optional


class OrganizationSchema(BaseModel):
    """Schema for organization creation/update."""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    status: str = "active"
    address: Optional[dict] = None


class OrganizationListSchema(BaseModel):
    """Schema for organization list response."""
    id: int
    name: str
    email: EmailStr
    status: str
    address: Optional[dict] = None 