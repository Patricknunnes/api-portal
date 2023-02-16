from pydantic import BaseModel
from typing import List
from uuid import UUID

from src.schemas.role_schema import RoleResponse


class AccessBase(BaseModel):
    id: UUID
    title: str
    description: str
    icon_path: str
    link_path: str

    class Config:
        orm_mode = True


class AccessResponse(AccessBase):
    allowed_roles: List[RoleResponse]


class AccessMeResponse(AccessBase):
    is_favorite: bool
