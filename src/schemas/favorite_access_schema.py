from uuid import UUID
from pydantic import BaseModel


class FavoriteAccessResponse(BaseModel):
    id: UUID
    access_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class FavoriteAccessPrimaryKeys(BaseModel):
    access_id: UUID
    user_id: UUID
