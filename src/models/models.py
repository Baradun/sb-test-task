from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Domain(Base):
    __tablename__ = "domains"
    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True, unique=True)

    visits = relationship("VisitsTime", back_populates="domain")


class VisitsTime(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("domains.id"))
    visit_time = Column(DateTime)

    domain = relationship("Domain", back_populates="visits")
