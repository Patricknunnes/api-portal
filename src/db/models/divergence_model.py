from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.settings.config import Base, GUID


class DivergenceModel(Base):
    __tablename__ = "divergences"

    id = Column(GUID(), primary_key=True, default=uuid4)
    name = Column(String(150), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(150), nullable=True)
    document = Column(String(50), nullable=True)
    role_id = Column(GUID(), ForeignKey("roles.id"))
    error = Column(String, nullable=False)

    role = relationship("RoleModel")
