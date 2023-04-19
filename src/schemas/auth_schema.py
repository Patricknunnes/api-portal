from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from src.schemas.role_schema import RoleResponse
from src.schemas.user_schema import UserMe


class BasicTokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenResponse(BasicTokenResponse):
    session_id: str
    token_type: str = 'Bearer'
    user: UserMe


class RefreshReqBody(BaseModel):
    refresh_token: str
    session_id: UUID


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
