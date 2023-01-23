from uuid import UUID
from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel

from src.schemas.role_schema import RoleResponse
from src.schemas.user_schema import User


class MessageCreateReqBody(BaseModel):
    title: str
    text: str
    expiration_date: Optional[str]
    role_permission: Optional[UUID]
    user_permission: Optional[UUID]
    is_important: Optional[bool]


class MessageCreate(MessageCreateReqBody):
    created_by: UUID


class MessageUpdateReqBody(BaseModel):
    title: Optional[str]
    text: Optional[str]
    expiration_date: Optional[str]
    role_permission: Optional[Union[UUID, str]]
    user_permission: Optional[Union[UUID, str]]
    is_important: Optional[bool]


class MessageUpdate(MessageUpdateReqBody):
    updated_by: UUID


class MessageResponse(BaseModel):
    id: UUID
    title: str
    text: str
    expiration_date: Optional[datetime]
    role: Optional[RoleResponse]
    user: Optional[User]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_important: bool

    class Config:
        orm_mode = True


class MessageResponsePaginate(BaseModel):
    page: int = 1
    total: int
    results: List[MessageResponse]
