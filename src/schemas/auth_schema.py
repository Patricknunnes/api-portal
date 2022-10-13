from pydantic import BaseModel
from typing import Optional

from src.schemas.role_schema import RoleResponse
from src.schemas.user_schema import UserResponse


class TokenResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = 'Bearer'


class ResponseSsoTotvs(BaseModel):
    user_name: Optional[str]
    key_totvs: Optional[str]


class ProfileResponse(BaseModel):
    name: str
    email: str
    role: str


class LoginBase(BaseModel):
    document: str
    password: str


class PermissionParams(BaseModel):
    user_role: RoleResponse
    path: str
    method: str
