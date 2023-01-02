from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from src.schemas.role_schema import RoleResponse
from src.schemas.user_schema import User


class MessageResponse(BaseModel):
    id: UUID
    title: str
    text: str
    expiration_date: Optional[datetime]
    role: Optional[RoleResponse]
    user: Optional[User]

    class Config:
        orm_mode = True


class MessageResponsePaginate(BaseModel):
    page: int = 1
    total: int
    results: List[MessageResponse]
