from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.patient import Patient
    from models.procedures import Procedure


class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = {
        "comment": "Faturas importadas da operadora São Lucas",
    }

    id_invoice: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        server_default=func.uuid_generate_v4(),
        comment="ID único criado automaticamente para cada fatura",
    )

    dt_service: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de realização do atendimento",
    )
    cd_patient: Mapped[str] = mapped_column(
        String(30),
        ForeignKey("patients.cd_patient"),
        nullable=False,
        comment="Código do paciente (código do beneficiário)",
    )
    cd_procedure: Mapped[str] = mapped_column(
        String(30),
        ForeignKey("procedures.cd_procedure"),
        nullable=False,
        comment="Código identificador único do procedimento (código TUSS)",
    )
    qt_procedure: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Quantidade do procedimento realizado"
    )
    vl_procedure: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="Valor total faturado do procedimento"
    )
    nr_page: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Página em que o registro é encontrado no relatório original",
    )
    dt_base: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Mês e ano de referencia"
    )
    nm_file: Mapped[str] = mapped_column(
        String(30), nullable=False, comment="Nome do arquivo de origem"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="Data e hora de criação do registro",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Data e hora da última atualização do registro",
    )

    patient: Mapped["Patient"] = relationship(back_populates="invoices")
    procedure: Mapped["Procedure"] = relationship(back_populates="invoices")

    def __repr__(self) -> str:
        return f"<Invoice(dt_service='{self.dt_service}', cd_patient='{self.cd_patient}', cd_procedure='{self.cd_procedure}', qt_procedure='{self.qt_procedure}', vl_procedure='{self.vl_procedure}')>"
