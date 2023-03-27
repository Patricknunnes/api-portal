from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, EmailStr

from src.schemas.role_schema import RoleResponse
from src.schemas.institution_schema import Institution


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
    role: RoleResponse
    institution: Institution

    class Config:
        orm_mode = True


class UserResponse(User):
    email: EmailStr
    phone: Optional[int]
    image: Optional[str]
    is_totvs: bool


class UserMe(UserResponse):
    document: str


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
    username: str
    role: RoleResponse
    institution: Institution
    error: str

    class Config:
        orm_mode = True


class DivergenceResponsePaginate(BaseModel):
    page: int = 1
    total: int
    results: List[UserDivergence]
