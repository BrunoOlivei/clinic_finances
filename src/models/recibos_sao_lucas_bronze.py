import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core import BronzeBase


class RecibosSaoLucasBronze(BronzeBase):
    __tablename__ = 'tb_recibos_sao_lucas'
    __table_args__ = {
        "schema": "brz",
        "comment": "Tabela de recibos importados da operadora São Lucas, na camada bronze",
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Identificador único do registro (UUID)",
    )
    dt_atendimento: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Data de realização do atendimento (formato: dd/mm/yyyy)",
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
    qt_procedimento: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Quantidade do procedimento realizado",
    )
    vl_procedimento: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Valor do procedimento realizado",
    )
    nr_pagina: Mapped[str] = mapped_column(
        String(3),
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
        comment="Nome do arquivo de origem do recibo",
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
    silver_exported: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Flag indicando se o registro foi exportado para a camada silver",
    )
    silver_date_export: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="Data e hora de exportação para a camada silver",
    )
