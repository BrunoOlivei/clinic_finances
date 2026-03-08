import uuid
from datetime import datetime

from sqlalchemy import UUID, Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core import BronzeBase


class SolicitacoesSaoLucasBronze(BronzeBase):
    """
    Data model for the "tb_solicitacoes_sao_lucas" table in the bronze layer,
    representing the raw data of claims imported from the São Lucas operator.
    This model includes fields for terminal, claim number, emission and attendance dates,
    beneficiary information, requester and provider details, procedure information,
    and control columns for tracking ingestion and export status.

    Args:
        BronzeBase (_type_): Base class for bronze layer models, providing common attributes and methods for all bronze tables.
    """

    __tablename__ = "tb_solicitacoes_sao_lucas"
    __table_args__ = {
        "schema": "brz",
        "comment": "Tabela de solicitações importadas da operadora São Lucas, na camada bronze",
    }
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Identificador único do registro (UUID)",
    )
    solicitacao: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Número da solicitação.",
    )
    data: Mapped[str] = mapped_column(
        String(19), nullable=False, comment="Data da abertura da solicitação (formato: dd/mm/yyyy)"
    )
    validade_solicitacao: Mapped[str] = mapped_column(
        String(10), nullable=False, comment="Data do vencimento da solicitação (formato: dd/mm/yyyy)"
    )
    solicitante: Mapped[str] = mapped_column(
        String(5), nullable=False, comment="Código do profissinal de saúde solicitante"
    )
    operador: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Código do usuário que registrou a solicitação no sistema",
    )
    terminal: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Nome do usuário master do sistema para identificação de onde partiu a solicitação",
    )
    solicitante_1: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Nome do profissional de saúde solicitante"
    )
    beneficiario: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        comment="Código do beneficiário (código do paciente)",
    )
    beneficiario_1: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Nome do beneficiário (nome do paciente)"
    )
    especialidade: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Especialidade do profissional de saúde solicitante",
    )
    procedimento: Mapped[str] = mapped_column(
        String(8), nullable=False, comment="Código do procedimento solicitado"
    )
    procedimento_1: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Nome do procedimento solicitado"
    )
    qtde_sol: Mapped[str] = mapped_column(
        String(3), nullable=False, comment="Quantidade do procedimento solicitado"
    )
    qtde_lib: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Quantidade do procedimento solicitado que foi liberado pela operadora",
    )
    qtde_exe: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Quantidade do procedimento solicitado que foi executado",
    )
    prestador: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Código do prestador (código do profissional ou instituição que realizou o procedimento)",
    )
    especialidade_prestador: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Especialidade do prestador que executou o procedimento solicitado",
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="Descrição do status da solicitação"
    )
    especificacao: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Descrições de especificações e orientações relacionadas ao procedimento solicitado, se disponíveis",
    )
    tipo_de_solicitacao: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Tipo de solicitação (ex: Consulta, Exame)",
    )
    operador_cancelamento: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Código do operador que cancelou a solicitação, se aplicável",
    )
    observacao: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Observações sobre a solicitação"
    )
    auditor: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Código do usuário que realizou a auditoria da solicitação, se disponível"
    )
    data_agendamento: Mapped[str] = mapped_column(
        String(10),
        nullable=True,
        comment="Data de agendamento para a realização do procedimento solicitado, se disponível (formato: dd/mm/yyyy)",
    )
    operador_agendamento: Mapped[str] = mapped_column(
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
