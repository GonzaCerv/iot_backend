"""User schema."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """User creation model."""

    name: str
    last_name: str
    email: EmailStr
    password: str
    is_active: bool
    is_admin: bool


class UserOut(BaseModel):
    """User output model."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    last_name: str
    email: EmailStr
    create_date: datetime
    is_active: bool
    is_admin: bool
