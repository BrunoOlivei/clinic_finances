from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.patient import Patient


class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"
    __table_args__ = {
        "comment": "Atendimentos realizados no período, importados da operadora São Lucas",
    }

    nr_claim: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        comment="Número do atendimento (guia)",
    )
    nr_request: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        comment="Número da solicitação",
    )
    cd_patient: Mapped[str] = mapped_column(
        String(30),
        ForeignKey("patients.cd_patient"),
        nullable=False,
        comment="Código do paciente (código do beneficiário)",
    )
    dt_issue: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de emissão do atendimento",
    )
    dm_service: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="Data e hora de realização do atendimento",
    )
    st_claim: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Status do atendimento (ex: Autorizada, Pendente)",
    )
    tp_claim: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Tipo do atendimento (ex: Consulta, Senha)",
    )
    fg_return: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment="Flag indicando se o atendimento é retorno",
    )
    cd_procedure: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Código do procedimento realizado",
    )
    nm_procedure: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Nome do procedimento realizado",
    )
    qt_procedure: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Quantidade do procedimento realizado",
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

    patient: Mapped["Patient"] = relationship(back_populates="insurance_claims")

    def __repr__(self) -> str:
        return (
            f"<InsuranceClaim(nr_claim='{self.nr_claim}', "
            f"cd_patient='{self.cd_patient}')>"
        )
