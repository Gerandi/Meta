# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
# Shared properties
class UserBase(BaseModel):
    email: EmailStr
# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
# Properties stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True # Replaces orm_mode
# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
# Additional properties to return via API
class User(UserInDBBase):
    pass # No extra fields needed for now