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


class UserSchemaValidate(BaseModel):
    role_id: UUID
    name: str
    email: EmailStr
    document: str
    password: str


class User(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


class UserResponse(User):
    email: EmailStr
    document: str
    phone: Optional[int]
    image: Optional[str]
    is_totvs: bool
    role: RoleResponse


class UserResponsePaginate(BaseModel):
    page: int = 1
    total: int
    user_response: List[UserResponse]


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[int]
    password: Optional[str]


class UserDivergence(BaseModel):
    name: str
    email: Optional[str]
    document: str
    username: str
    role: RoleResponse
    error: str


class DivergenceResponsePaginate(BaseModel):
    page: int = 1
    total: int
    results: List[UserDivergence]
