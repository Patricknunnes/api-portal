from uuid import UUID
from pydantic import BaseModel


class MessageUserResponse(BaseModel):
    id: UUID
    message_id: UUID
    user_id: UUID
    message_read: bool

    class Config:
        orm_mode = True


class MessageUserPrimaryKeys(BaseModel):
    message_id: UUID
    user_id: UUID
