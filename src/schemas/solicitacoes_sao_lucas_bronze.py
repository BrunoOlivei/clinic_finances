from datetime import datetime

from pydantic import BaseModel, Field


class SolicitacoesSaoLucasBronzeSchema(BaseModel):
    solicitacao: str = Field(..., description="Número da solicitação")
    data: str = Field(
        ..., description="Data da abertura da solicitação (formato: dd/mm/yyyy)"
    )
    validade_solicitacao: str = Field(
        ..., description="Data do vencimento da solicitação (formato: dd/mm/yyyy)"
    )
    solicitante: str = Field(
        ..., description="Código do profissional de saúde solicitante"
    )
    operador: str = Field(
        ..., description="Código do usuário que registrou a solicitação no sistema"
    )
    terminal: str | None = Field(
        None,
        description="Nome do usuário master do sistema para identificação de onde partiu a solicitação",
    )
    solicitante_1: str = Field(
        ..., description="Nome do profissional de saúde solicitante"
    )
    beneficiario: str = Field(
        ..., description="Código do beneficiário (código do paciente)"
    )
    beneficiario_1: str | None = Field(
        None, description="Nome do beneficiário (nome do paciente)"
    )
    especialidade: str = Field(
        ..., description="Especialidade do profissional de saúde solicitante"
    )
    procedimento: str = Field(..., description="Código do procedimento solicitado")
    procedimento_1: str = Field(..., description="Nome do procedimento solicitado")
    qtde_sol: str = Field(..., description="Quantidade do procedimento solicitado")
    qtde_lib: str = Field(
        ...,
        description="Quantidade do procedimento solicitado que foi liberado pela operadora",
    )
    qtde_exe: str = Field(
        ..., description="Quantidade do procedimento solicitado que foi executado"
    )
    prestador: str | None = Field(
        None,
        description="Código do prestador (código do profissional ou instituição que realizou o procedimento)",
    )
    especialidade_prestador: str | None = Field(
        None,
        description="Especialidade do prestador que executou o procedimento solicitado",
    )
    status: str = Field(..., description="Descrição do status da solicitação")
    especificacao: str | None = Field(
        None,
        description="Descrições de especificações e orientações relacionadas ao procedimento solicitado, se disponíveis",
    )
    tipo_de_solicitacao: str = Field(
        ..., description="Tipo de solicitação (ex: Consulta, Exame)"
    )
    operador_cancelamento: str | None = Field(
        None, description="Código do operador que cancelou a solicitação, se aplicável"
    )
    observacao: str | None = Field(None, description="Observações sobre a solicitação")
    auditor: str | None = Field(
        None,
        description="Código do usuário que realizou a auditoria da solicitação, se disponível",
    )
    data_agendamento: str | None = Field(
        None,
        description="Data de agendamento para a realização do procedimento solicitado, se disponível (formato: dd/mm/yyyy)",
    )
    operador_agendamento: str | None = Field(
        None, description="Código do operador que realizou o agendamento, se disponível"
    )
    dt_base: int = Field(..., description="Mês e ano base do arquivo (formato: yyyymm)")
    file_name: str = Field(..., description="Nome do arquivo de origem do atendimento")
    silver_exported: bool = Field(
        False, description="Indica se o atendimento foi exportado para a camada silver"
    )
    silver_date_export: datetime | None = Field(
        None,
        description="Data e hora de exportação para a camada silver, se aplicável)",
    )
