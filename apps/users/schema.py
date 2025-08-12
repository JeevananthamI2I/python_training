from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date

class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    password_confirm: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    organization: Optional[int] = None
    role: Optional[int] = None
    status: str = "active"

    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserListSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    phone: Optional[str] = None
    status: str
