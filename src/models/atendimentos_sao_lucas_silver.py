from datetime import date, datetime, time
import uuid

from sqlalchemy import Boolean, Date, DateTime, Integer, String, Time, UUID, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core import SilverBase


class AtendimentosSaoLucasSilver(SilverBase):
    __tablename__ = "tb_atendimentos_sao_lucas"
    __table_args__ = {
        "schema": "slv",
        "comment": "Tabela de atendimentos importados da operadora São Lucas, na camada silver",
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Identificador único do registro (UUID)",
    )
    cd_terminal: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        comment="Terminal de atendimento (ex: 0001, 0002)",
    )
    nr_guia: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Número do atendimento (guia)"
    )
    dt_emissao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de emissão da guia (formato: dd/mm/yyyy)",
    )
    dt_atendimento: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de realização do atendimento (formato: dd/mm/yyyy)",
    )
    hr_atendimento: Mapped[time] = mapped_column(
        Time,
        nullable=False,
        comment="Horário de realização do atendimento (formato: hh:mm:ss)",
    )
    dt_emissao_tiss: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de emissão da guia no formato TISS (formato: d/mm/yyyy)",
    )
    cd_beneficiario: Mapped[str] = mapped_column(
        String(18),
        nullable=False,
        comment="Código do beneficiário (código do paciente)",
    )
    nm_beneficiario: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Nome do beneficiário (nome do paciente)",
    )
    ds_endereco_beneficiario: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Endereço do beneficiário (endereço do paciente)",
    )
    cd_solicitante: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Código do solicitante (código do profissional de saúde que solicitou o atendimento)",
    )
    nm_solicitante: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do solicitante (nome do profissional de saúde que solicitou o atendimento)",
    )
    ds_especialidade: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Especialidade do atendimento (ex: Dermatologia, Pediatria)",
    )
    st_atendimento: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Status do atendimento (ex: AUTORIZADA, Pendente)",
    )
    tp_atendimento: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Tipo do atendimento (ex: Consulta, Senha)",
    )
    fg_retorno: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment="Flag indicando se o atendimento é retorno",
    )
    cd_senha_terapia: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Número da senha de terapia, se aplicável",
    )
    cd_procedimento: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        comment="Código do procedimento realizado",
    )
    ds_procedimento: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do procedimento realizado",
    )
    qt_procedimento: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Quantidade do procedimento realizado",
    )
    qt_sessoes_executadas: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment="Número de sessões executadas, se aplicável",
    )
    cd_prestador: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Código do prestador (código do profissional de saúde que realizou o atendimento)",
    )
    nm_prestador: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do prestador (nome do profissional de saúde que realizou o atendimento)",
    )
    ds_especialidade_prestador: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Especialidade do prestador (ex: Dermatologia, Pediatria)",
    )
    ds_indicacao_clinica: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Indicação clínica para o atendimento, se disponível",
    )
    st_export: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        comment="Indica se o atendimento foi exportado no sistema de origem",
    )
    dt_export: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de exportação do atendimento no sistema de origem (formato: dd/mm/yyyy)",
    )
    dt_senha: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de geração da senha, se aplicável",
    )
    cd_operador_execucao: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Código do operador que executou o atendimento, se disponível",
    )
    cd_operador_senha: Mapped[str] = mapped_column(
        String(6),
        nullable=True,
        comment="Código do operador que gerou a senha, se aplicável",
    )
    cd_operador_cancelamento: Mapped[str] = mapped_column(
        String(6),
        nullable=True,
        comment="Código do operador que cancelou o atendimento, se aplicável",
    )
    ds_observacao: Mapped[str] = mapped_column(
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
