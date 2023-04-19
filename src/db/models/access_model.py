from sqlalchemy import Column, String, TIMESTAMP, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from src.db.settings.config import Base, GUID
from src.db.models.role_model import RoleModel

access_role = Table(
    'accesses_roles',
    Base.metadata,
    Column('access_id', GUID(), ForeignKey('accesses.id'), nullable=False),
    Column('role_id', GUID(), ForeignKey('roles.id'), nullable=False)
)


class AccessModel(Base):
    __tablename__ = 'accesses'

    id = Column(GUID(), primary_key=True, default=uuid4)
    title = Column(String(50), nullable=False)
    description = Column(String(150), nullable=False)
    icon_path = Column(String(), nullable=False)
    link_path = Column(String(), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    allowed_roles = relationship(RoleModel, secondary=access_role, backref='accesses')
