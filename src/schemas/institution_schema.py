from uuid import UUID
from pydantic import BaseModel


class Institution(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
