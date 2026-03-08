import uuid
from datetime import datetime, date

from sqlalchemy import UUID, DateTime, Integer, String, text, Date
from sqlalchemy.orm import Mapped, mapped_column

from src.core import SilverBase


class SolicitacoesSaoLucasSilver(SilverBase):
    """
    Data model for the "tb_solicitacoes_sao_lucas" table in the silver layer,
    representing the processed data of claims imported from the São Lucas operator.
    This model includes fields for terminal, claim number, emission and attendance dates,
    beneficiary information, requester and provider details, procedure information,
    and control columns for tracking ingestion and export status.

    Args:
        SilverBase (_type_): Base class for silver layer models, providing common attributes and methods for all silver tables.
    """

    __tablename__ = "tb_solicitacoes_sao_lucas"
    __table_args__ = {
        "schema": "slv",
        "comment": "Tabela de solicitações importadas da operadora São Lucas, na camada silver",
    }
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Identificador único do registro (UUID)",
    )
    nr_solicitacao: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Número da solicitação.",
    )
    dt_solicitacao: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="Data da abertura da solicitação"
    )
    dt_validade_solicitacao: Mapped[date] = mapped_column(
        Date, nullable=False, comment="Data do vencimento da solicitação"
    )
    cd_solicitante: Mapped[str] = mapped_column(
        String(5), nullable=False, comment="Código do profissinal de saúde solicitante"
    )
    cd_operador: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Código do usuário que registrou a solicitação no sistema",
    )
    nm_terminal: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Nome do usuário master do sistema para identificação de onde partiu a solicitação",
    )
    nm_solicitante: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Nome do profissional de saúde solicitante"
    )
    cd_beneficiario: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        comment="Código do beneficiário (código do paciente)",
    )
    nm_beneficiario: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Nome do beneficiário (nome do paciente)"
    )
    ds_especialidade: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Especialidade do profissional de saúde solicitante",
    )
    cd_procedimento: Mapped[str] = mapped_column(
        String(8), nullable=False, comment="Código do procedimento solicitado"
    )
    nm_procedimento: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Nome do procedimento solicitado"
    )
    qt_solicitado: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Quantidade do procedimento solicitado"
    )
    qt_liberado: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Quantidade do procedimento solicitado que foi liberado pela operadora",
    )
    qt_executado: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Quantidade do procedimento solicitado que foi executado",
    )
    cd_prestador: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Código do prestador (código do profissional ou instituição que realizou o procedimento)",
    )
    ds_especialidade_prestador: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Especialidade do prestador que executou o procedimento solicitado",
    )
    st_solicitacao: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Descrição do status da solicitação"
    )
    ds_especificacao: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Descrições de especificações e orientações relacionadas ao procedimento solicitado, se disponíveis",
    )
    tp_solicitacao: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Tipo de solicitação (ex: Consulta, Exame)",
    )
    cd_operador_cancelamento: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Código do operador que cancelou a solicitação, se aplicável",
    )
    ds_observacao: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Observações sobre a solicitação"
    )
    cd_auditor: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Código do usuário que realizou a auditoria da solicitação, se disponível"
    )
    dt_agendamento: Mapped[date] = mapped_column(
        Date,
        nullable=True,
        comment="Data de agendamento para a realização do procedimento solicitado, se disponível",
    )
    cd_operador_agendamento: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Código do operador que realizou o agendamento, se disponível",
    )
    dt_base: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Mês e ano base do arquivo no formato YYYYMM (ex: 202401)",
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do arquivo de origem do atendimento",
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
