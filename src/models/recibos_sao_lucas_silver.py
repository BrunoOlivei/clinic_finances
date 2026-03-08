import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, UUID, Date, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core import SilverBase


class RecibosSaoLucasSilver(SilverBase):
    __tablename__ = "tb_recibos_sao_lucas"
    __table_args__ = {
        "schema": "slv",
        "comment": "Tabela de recibos importados da operadora São Lucas, na camada silver",
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Identificador único do registro (UUID)",
    )
    dt_atendimento: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de realização do atendimento",
    )
    cd_beneficiario: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        comment="Código do beneficiário (código do paciente)",
    )
    cd_procedimento: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        comment="Código do procedimento realizado",
    )
    qt_procedimento: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Quantidade do procedimento realizado",
    )
    vl_procedimento: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
        comment="Valor do procedimento realizado",
    )
    nr_pagina: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Número da página do relatório de atendimento onde o procedimento está descrito",
    )
    dt_base: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Mês e ano base do arquivo no formato YYYYMM (ex: 202401)",
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do arquivo de origem do registro",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="Data e hora de criação do registro",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="Data e hora de última atualização do registro",
    )
