from sqlalchemy import Column, Integer, String, Text, ForeignKey, Interval, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .database import Base
from enum import Enum


class StatusEnum(Enum):
    DISPONIBLE = "disponible"
    NON_DISPONIBLE = "non_disponible"
    REFUSE = "refuse"

class Programme(Base):
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    codeProgramme = Column(String(20), unique=True, index=True, nullable=False)
    nomProgramme = Column(String(255), nullable=False)
    descProgramme = Column(Text, nullable=True)
    publicCible = Column(Text, nullable=True)
    dureeProgramme = Column(Interval, nullable=True)
    dateCreation = Column(DateTime(timezone=True))
    prixProgramme = Column(Numeric(5, 2), nullable=True)
    status = Column(
        SQLEnum(StatusEnum, name="status_enum"),
        nullable=False,
        default=StatusEnum.DISPONIBLE       
    )

    courses = relationship("Cours", back_populates="programme", cascade="all, delete-orphan")


class Cours(Base):
    __tablename__ = "cours"

    id = Column(Integer, primary_key=True, index=True)
    codeCours = Column(String(20), unique=True, index=True, nullable=False)
    titreCours = Column(String(255), nullable=False)
    prixCours = Column(Numeric(5, 2), nullable=True)
    dateCreation = Column(DateTime(timezone=True))


    programme_id = Column(Integer, ForeignKey("programmes.id"), nullable=False)
    programme = relationship("Programme", back_populates="cours")
