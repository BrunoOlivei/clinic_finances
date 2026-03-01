from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.insurance_claim import InsuranceClaim
    from models.invoice import Invoice


class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = {
        "comment": "Cadastro de pacientes atendidos na clínica",
    }

    cd_patient: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
        comment="Código identificador único do paciente (código do beneficiário)",
    )
    nm_patient: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
        comment="Nome completo do paciente",
    )
    ds_address: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        comment="Endereço residencial do paciente",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="Data e hora de criação do registro",
    )

    insurance_claims: Mapped[list["InsuranceClaim"]] = relationship(
        back_populates="patient"
    )
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="patient")

    def __repr__(self) -> str:
        return (
            f"<Patient(cd_patient='{self.cd_patient}', nm_patient='{self.nm_patient}')>"
        )
