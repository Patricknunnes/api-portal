from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class ProfileResponse(BaseModel):
    name: str
    email: str
    role: str


class LoginBase(BaseModel):
    email: str
    password: str
