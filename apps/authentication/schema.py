from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginSchema(BaseModel):
    """Schema for login requests."""
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str
    password: str
    password_confirm: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization: Optional[int] = None
    role: Optional[int] = None 