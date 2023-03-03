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
    document: str
    role: RoleResponse

    class Config:
        orm_mode = True


class UserResponse(User):
    email: EmailStr
    phone: Optional[int]
    image: Optional[str]
    is_totvs: bool


class UserResponsePaginate(BaseModel):
    page: int = 1
    total: int
    results: List[UserResponse]


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[int]
    password: Optional[str]


class UserDivergence(BaseModel):
    id: UUID
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
    results: List[UserDivergence]
