from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.settings.config import Base, GUID


class DivergenceModel(Base):
    __tablename__ = 'divergences'

    id = Column(GUID(), primary_key=True, default=uuid4)
    name = Column(String(150), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(150), nullable=True)
    document = Column(String(50), nullable=True)
    role_id = Column(GUID(), ForeignKey('roles.id'))
    error = Column(String, nullable=False)
    institution_id = Column(
        GUID(),
        ForeignKey('institutions.id'),
        default='dcef34bf-2cc6-4d67-b6af-803e7e33d0f3'
    )

    role = relationship('RoleModel')
    institution = relationship('InstitutionModel')
