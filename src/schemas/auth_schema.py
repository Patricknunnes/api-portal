from pydantic import BaseModel
from typing import Optional

from src.schemas.role_schema import RoleResponse
from src.schemas.user_schema import UserMe


class TokenResponse(BaseModel):
    user: UserMe
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
    username: str
    password: str


class PermissionParams(BaseModel):
    user_role: RoleResponse
    path: str
    method: str
