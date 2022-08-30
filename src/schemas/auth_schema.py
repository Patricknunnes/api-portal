from pydantic import BaseModel

from src.schemas.role_schema import RoleResponse


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


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
