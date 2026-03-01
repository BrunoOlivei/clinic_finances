from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models.insurance_claim import InsuranceClaim
    from models.invoice import Invoice


class Procedure(Base):
    __tablename__ = "procedures"
    __table_args__ = {
        "comment": "Cadastro de procedimentos realizados na clínica",
    }

    cd_procedure: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
        comment="Código identificador único do procedimento (código TUSS)",
    )
    nm_procedure: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
        comment="Nome do procedimento",
    )
    vl_procedure: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Valor do procedimento (preço de tabela)",
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

    insurance_claims: Mapped[list["InsuranceClaim"]] = relationship(
        back_populates="procedure",
    )
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="procedure")
    
    def __repr__(self) -> str:
        return f"<Procedure(cd_procedure='{self.cd_procedure}', nm_procedure='{self.nm_procedure}', vl_procedure='{self.vl_procedure}')>"
