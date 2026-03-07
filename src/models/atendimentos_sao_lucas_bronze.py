from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core import BronzeBase


class AtendimentosSaoLucasBronze(BronzeBase):
    """
    Data model for the "tb_atendimentos_sao_lucas" table in the bronze layer,
    representing the raw data of attendances imported from the São Lucas operator.
    This model includes fields for terminal, guide number, emission and attendance dates,
    beneficiary information, requester and provider details, procedure information,
    and control columns for tracking ingestion and export status.

    Args:
        BronzeBase (_type_): Base class for bronze layer models, providing common attributes and methods for all bronze tables.
    """

    __tablename__ = "tb_atendimentos_sao_lucas"
    __table_args__ = {
        "schema": "brz",
        "comment": "Tabela de atendimentos importados da operadora São Lucas, na camada bronze",
    }

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=func.uuid_generate_v4(),
        comment="Identificador único do registro (UUID)",
    )
    terminal: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        comment="Terminal de atendimento (ex: 0001, 0002)",
    )
    guia: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        comment="Número do atendimento (guia)",
    )
    emissao: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Data de emissão da guia (formato: dd/mm/yyyy)",
    )
    atendimento: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Data de realização do atendimento (formato: dd/mm/yyyy)",
    )
    horario: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        comment="Horário de realização do atendimento (formato: hh:mm:ss)",
    )
    emissao_tiss: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Data de emissão da guia no formato TISS (formato: d/mm/yyyy)",
    )
    cd_beneficiario: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        comment="Código do beneficiário (código do paciente)",
    )
    beneficiario: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do beneficiário (nome do paciente)",
    )
    endereco_beneficiario: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Endereço do beneficiário (endereço do paciente)",
    )
    solicitante: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Código do solicitante (código do profissional de saúde que solicitou o atendimento)",
    )
    solicitante_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do solicitante (nome do profissional de saúde que solicitou o atendimento)",
    )
    especialidade: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Especialidade do atendimento (ex: Dermatologia, Pediatria)",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Status do atendimento (ex: AUTORIZADA, Pendente)",
    )
    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Tipo do atendimento (ex: Consulta, Senha)",
    )
    retorno: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        comment="Flag indicando se o atendimento é retorno (ex: Sim, Não)",
    )
    senha_terapia: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Número da senha de terapia, se aplicável",
    )
    procedimento: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        comment="Código do procedimento realizado",
    )
    procedimento_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do procedimento realizado",
    )
    quantidade: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Quantidade do procedimento realizado",
    )
    sessoes_executadas: Mapped[str] = mapped_column(
        String(10),
        nullable=True,
        comment="Número de sessões executadas, se aplicável",
    )
    prestador: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Código do prestador (código do profissional de saúde que realizou o atendimento)",
    )
    prestador_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do prestador (nome do profissional de saúde que realizou o atendimento)",
    )
    especialidade_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Especialidade do prestador (ex: Dermatologia, Pediatria)",
    )
    indicacao_clinica: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Indicação clínica para o atendimento, se disponível",
    )
    status_export: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        comment="Indica se o atendimento foi exportado no sistema de origem",
    )
    dt_export: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Data de exportação do atendimento no sistema de origem (formato: dd/mm/yyyy)",
    )
    dt_senha: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Data de geração da senha, se aplicável (formato: dd/mm/yyyy)",
    )
    operador_execucao: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Código do operador que executou o atendimento, se disponível",
    )
    operador_senha: Mapped[str] = mapped_column(
        String(6),
        nullable=True,
        comment="Código do operador que gerou a senha, se aplicável",
    )
    operador_canc: Mapped[str] = mapped_column(
        String(6),
        nullable=True,
        comment="Código do operador que cancelou o atendimento, se aplicável",
    )
    observacao: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Observações adicionais sobre o atendimento, se disponíveis",
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
