from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(GUID(), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False)
    text = Column(String, nullable=False)
    expiration_date = Column(TIMESTAMP, nullable=True)
    role_permission = Column(GUID(), ForeignKey('roles.id'), nullable=True)
    user_permission = Column(GUID(), ForeignKey('users.id'), nullable=True)
    is_important = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.current_timestamp())
    created_by = Column(GUID(), ForeignKey('users.id'), nullable=True)
    updated_by = Column(GUID(), ForeignKey('users.id'), nullable=True)

    role = relationship("RoleModel", foreign_keys='MessageModel.role_permission')
    user = relationship("UserModel", foreign_keys='MessageModel.user_permission')
    author = relationship("UserModel", foreign_keys='MessageModel.created_by')
    update_author = relationship("UserModel", foreign_keys='MessageModel.updated_by')

    message_users = relationship(
        'MessageUserModel',
        back_populates='message',
        cascade='all, delete'
    )
