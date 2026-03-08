from datetime import datetime

from pydantic import BaseModel, Field


class AtendimentoSaoLucasBronzeSchema(BaseModel):
    terminal: str = Field(..., description="Terminal de atendimento (ex: 0001, 0002)")
    guia: str = Field(..., description="Número do atendimento (guia)")
    emissao: str = Field(
        ..., description="Data de emissão da guia (formato: dd/mm/yyyy)"
    )
    atendimento: str = Field(
        ..., description="Data de realização do atendimento (formato: dd/mm/yyyy)"
    )
    horario: str = Field(
        ..., description="Horário de realização do atendimento (formato: HH:MM)"
    )
    emissao_tiss: str = Field(
        ..., description="Data de emissão da guia no formato TISS (formato: d/mm/yyyy)"
    )
    cd_beneficiario: str = Field(
        ..., description="Código do beneficiário (código do paciente)"
    )
    beneficiario: str | None = Field(
        None, description="Nome do beneficiário (nome do paciente)"
    )
    endereco_beneficiario: str | None = Field(
        None, description="Endereço do beneficiário (endereço do paciente)"
    )
    solicitante: str = Field(
        ...,
        description="Código do solicitante (código do profissional de saúde que solicitou o atendimento)",
    )
    solicitante_1: str = Field(
        ...,
        description="Nome do solicitante (nome do profissional de saúde que solicitou o atendimento)",
    )
    especialidade: str = Field(
        ..., description="Especialidade do atendimento (ex: Dermatologia, Pediatria)"
    )
    status: str = Field(
        ..., description="Status do atendimento (ex: Realizado, Cancelado)"
    )
    tipo: str = Field(..., description="Tipo do atendimento (ex: Consulta, Exame)")
    retorno: str = Field(..., description="Indicação de retorno (Sim ou Não)")
    senha_terapia: str | None = Field(
        None, description="Número da senha de terapia, se aplicável"
    )
    procedimento: str = Field(..., description="Código do procedimento realizado")
    procedimento_1: str = Field(..., description="Nome do procedimento realizado")
    quantidade: str = Field(..., description="Quantidade do procedimento realizado")
    sessoes_executadas: str | None = Field(
        None, description="Número de sessões executadas, se aplicável"
    )
    prestador: str = Field(
        ...,
        description="Código do prestador (código do profissional de saúde que realizou o atendimento)",
    )
    prestador_1: str = Field(
        ...,
        description="Nome do prestador (nome do profissional de saúde que realizou o atendimento)",
    )
    especialidade_1: str = Field(
        ..., description="Especialidade do prestador (ex: Dermatologia, Pediatria)"
    )
    indicacao_clinica: str | None = Field(
        None, description="Indicação clínica para o procedimento realizado"
    )
    status_export: str = Field(
        ..., description="Indica se o atendimento foi exportado no sistema de origem"
    )
    dt_export: str = Field(
        ...,
        description="Data de exportação do atendimento no sistema de origem (formato: dd/mm/yyyy)",
    )
    dt_senha: str = Field(
        ...,
        description="Data de geração da senha de terapia, se aplicável (formato: dd/mm/yyyy)",
    )
    operador_execucao: str = Field(
        ..., description="Código do operador que executou o atendimento, se disponível"
    )
    operador_senha: str | None = Field(
        None, description="Código do operador que gerou a senha, se disponível"
    )
    operador_canc: str | None = Field(
        None, description="Código do operador que cancelou o atendimento, se disponível"
    )
    observacao: str | None = Field(
        None, description="Observações adicionais sobre o atendimento, se disponíveis"
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
