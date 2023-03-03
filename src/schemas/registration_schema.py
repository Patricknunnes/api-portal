from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import List
from uuid import UUID

from src.schemas.user_schema import User


class StatusEnum(Enum):
    ANALYSIS = 'ANALYSIS'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class RegistrationCreateBody(BaseModel):
    email: EmailStr
    birthdate: str


class RegistrationCreateModel(RegistrationCreateBody):
    document: str
    status: StatusEnum = StatusEnum.ANALYSIS
    service: str


class RegistrationUpdateBody(BaseModel):
    status: StatusEnum


class Registration(BaseModel):
    id: UUID
    service: str
    user: User
    status: StatusEnum

    class Config:
        orm_mode = True
        use_enum_values = True


class RegistrationResponse(Registration):
    email: EmailStr
    birthdate: datetime


class RegistrationResponsePaginate(BaseModel):
    page: int = 1
    total: int
    results: List[RegistrationResponse]
