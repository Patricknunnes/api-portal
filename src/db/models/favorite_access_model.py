from uuid import uuid4
from sqlalchemy import TIMESTAMP, Column, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.db.settings.config import GUID, Base


class FavoriteAccessModel(Base):
    __tablename__ = 'favorite_accesses'

    id = Column(GUID(), unique=True, index=True, default=uuid4)
    access_id = Column(GUID(), ForeignKey('accesses.id'), primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.id'), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    access = relationship('AccessModel')
    user = relationship('UserModel')
