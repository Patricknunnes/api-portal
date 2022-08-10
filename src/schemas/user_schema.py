from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr

from src.schemas.role_schema import RoleResponse


class UserBase(BaseModel):
    role_id: UUID
    name: str
    email: EmailStr
    document: str
    phone: Optional[int]
    password: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    document: str
    phone: int
    role: RoleResponse

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    document: Optional[str]
    phone: Optional[int]
    role_id: Optional[UUID]

    class Config:
        orm_mode = True
