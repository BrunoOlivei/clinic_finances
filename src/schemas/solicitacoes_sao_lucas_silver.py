from datetime import date, datetime

from pydantic import BaseModel, Field


class SolicitacoesSaoLucasSilverSchema(BaseModel):
    nr_solicitacao: int = Field(..., description="Número da solicitação")
    dt_solicitacao: datetime = Field(..., description="Data da abertura da solicitação")
    dt_validade_solicitacao: date = Field(
        ..., description="Data do vencimento da solicitação"
    )
    cd_solicitante: str = Field(
        ..., description="Código do profissional de saúde solicitante"
    )
    cd_operador: str = Field(
        ..., description="Código do usuário que registrou a solicitação no sistema"
    )
    nm_terminal: str | None = Field(
        None,
        description="Nome do usuário master do sistema para identificação de onde partiu a solicitação",
    )
    nm_solicitante: str = Field(
        ..., description="Nome do profissional de saúde solicitante"
    )
    cd_beneficiario: str = Field(
        ..., description="Código do beneficiário (código do paciente)"
    )
    nm_beneficiario: str | None = Field(
        None, description="Nome do beneficiário (nome do paciente)"
    )
    ds_especialidade: str = Field(
        ..., description="Especialidade do profissional de saúde solicitante"
    )
    cd_procedimento: str = Field(..., description="Código do procedimento solicitado")
    nm_procedimento: str = Field(..., description="Nome do procedimento solicitado")
    qt_solicitado: int = Field(..., description="Quantidade do procedimento solicitado")
    qt_liberado: int = Field(
        ...,
        description="Quantidade do procedimento solicitado que foi liberado pela operadora",
    )
    qt_executado: int = Field(
        ..., description="Quantidade do procedimento solicitado que foi executado"
    )
    cd_prestador: str | None = Field(
        None,
        description="Código do prestador (código do profissional ou instituição que realizou o procedimento)",
    )
    ds_especialidade_prestador: str | None = Field(
        None,
        description="Especialidade do prestador que executou o procedimento solicitado",
    )
    st_solicitacao: str = Field(..., description="Descrição do status da solicitação")
    ds_especificacao: str | None = Field(
        None,
        description="Descrições de especificações e orientações relacionadas ao procedimento solicitado, se disponíveis",
    )
    tp_solicitacao: str = Field(
        ..., description="Tipo de solicitação (ex: Consulta, Exame)"
    )
    cd_operador_cancelamento: str | None = Field(
        None, description="Código do operador que cancelou a solicitação, se aplicável"
    )
    ds_observacao: str | None = Field(
        None, description="Observações sobre a solicitação"
    )
    cd_auditor: str | None = Field(
        None,
        description="Código do usuário que realizou a auditoria da solicitação, se disponível",
    )
    dt_agendamento: date | None = Field(
        None,
        description="Data de agendamento para a realização do procedimento solicitado, se disponível (formato: dd/mm/yyyy)",
    )
    cd_operador_agendamento: str | None = Field(
        None, description="Código do operador que realizou o agendamento, se disponível"
    )
    dt_base: int = Field(..., description="Mês e ano base do arquivo (formato: yyyymm)")
    file_name: str = Field(..., description="Nome do arquivo de origem do atendimento")
