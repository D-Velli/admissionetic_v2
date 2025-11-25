from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.sql import func

from .database import Base


class TypeAdmissionEnum(str, Enum):
    PROGRAMME = "programme"
    COURS = "cours"


class StatutAdmissionEnum(str, Enum):
    EN_ATTENTE = "en_attente"
    ACCEPTEE = "acceptee"
    REFUSEE = "refusee"
    ANNULEE = "annulee"


class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)

    # Référence à l'utilisateur venant de user_service
    user_id = Column(Integer, index=True, nullable=False)

    # Type : admission à un programme ou à un cours
    type_admission = Column(
        SQLEnum(TypeAdmissionEnum, name="type_admission_enum"),
        nullable=False,
    )

    # IDs des ressources externes (autres microservices)
    programme_id = Column(Integer, nullable=True, index=True)
    cours_id = Column(Integer, nullable=True, index=True)

    # Infos métier
    statut = Column(
        SQLEnum(StatutAdmissionEnum, name="statut_admission_enum"),
        nullable=False,
        default=StatutAdmissionEnum.EN_ATTENTE,
    )

    commentaire = Column(Text, nullable=True)

    date_demande = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )

    date_maj = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
