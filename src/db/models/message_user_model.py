from uuid import uuid4
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.db.settings.config import GUID, Base


class MessageUserModel(Base):
    __tablename__ = 'messages_users'

    id = Column(GUID(), unique=True, index=True, default=uuid4)
    message_id = Column(GUID(), ForeignKey('messages.id'), primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.id'), primary_key=True)
    message_read = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    message = relationship('MessageModel')
    user = relationship('UserModel')
