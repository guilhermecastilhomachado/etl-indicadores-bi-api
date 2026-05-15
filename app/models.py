from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Pais(Base):
    __tablename__ = "paises"

    id = Column(Integer, primary_key=True, index=True)
    codigo_iso3 = Column(String(3), nullable=False, unique=True, index=True)
    nome = Column(String(120), nullable=False)

    registros = relationship("RegistroIndicador", back_populates="pais")


class Indicador(Base):
    __tablename__ = "indicadores"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), nullable=False, unique=True, index=True)
    nome = Column(String(180), nullable=False)
    fonte = Column(String(120), nullable=True)

    registros = relationship("RegistroIndicador", back_populates="indicador")


class RegistroIndicador(Base):
    __tablename__ = "registros_indicadores"

    id = Column(Integer, primary_key=True, index=True)

    pais_id = Column(Integer, ForeignKey("paises.id"), nullable=False)
    indicador_id = Column(Integer, ForeignKey("indicadores.id"), nullable=False)

    ano = Column(Integer, nullable=False, index=True)
    valor = Column(Numeric(20, 2), nullable=False)

    data_carga = Column(DateTime, nullable=False, default=datetime.utcnow)

    pais = relationship("Pais", back_populates="registros")
    indicador = relationship("Indicador", back_populates="registros")

    __table_args__ = (
        UniqueConstraint(
            "pais_id",
            "indicador_id",
            "ano",
            name="uq_registro_pais_indicador_ano"
        ),
    )