from pydantic import BaseModel
from typing import Optional


class AddressSchema(BaseModel):
    """Schema for address creation/update."""
    street_address: Optional[str] = None
    city: str
    state: str
    pincode: Optional[str] = None
    country: Optional[str] = None


class AddressListSchema(BaseModel):
    """Schema for address list response."""
    id: int
    street_address: Optional[str] = None
    city: str
    state: str
    pincode: Optional[str] = None
    country: Optional[str] = None 