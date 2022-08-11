from pydantic import BaseModel

from src.schemas.user_schema import UserResponse


class TokenResponse(BaseModel):
    access_token: str


class ProfileResponse(BaseModel):
    name: str
    email: str
    role: str


class LoginBase(BaseModel):
    email: str
    password: str
