from uuid import UUID
from typing import Optional, List
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


class UserSchemaValidate(BaseModel):
    role_id: UUID
    name: str
    email: EmailStr
    document: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    document: str
    phone: Optional[int]
    image: Optional[str]
    is_totvs: bool
    role: RoleResponse

    class Config:
        orm_mode = True


class UserResponsePaginate(BaseModel):
    page: int = 1
    total: int
    user_response: List[UserResponse]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[int]
    password: Optional[str]

    class Config:
        orm_mode = True


class UserDivergence(BaseModel):
    name: str
    email: Optional[str]
    document: str
    username: str
    role: RoleResponse
    error: str

    class Config:
        orm_mode = True

class DivergenceResponsePaginate(BaseModel):
    page: int = 1
    total: int
    divergences: List[UserDivergence]

    class Config:
        orm_mode = True
