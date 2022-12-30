from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey

from src.db.settings.config import Base, GUID


class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(GUID(), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False)
    text = Column(String, nullable=False)
    expiration_date = Column(TIMESTAMP, nullable=True)
    role_permission = Column(GUID(), ForeignKey('roles.id'), nullable=True)
    user_permission = Column(GUID(), ForeignKey('users.id'), nullable=True)
