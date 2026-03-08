from datetime import date, time

from pydantic import BaseModel, Field


class AtendimentoSaoLucasSilverSchema(BaseModel):
    cd_terminal: str = Field(
        ..., description="Terminal de atendimento (ex: 0001, 0002)"
    )
    nr_guia: int = Field(..., description="Número do atendimento (guia)")
    dt_emissao: date = Field(
        ..., description="Data de emissão da guia (formato: dd/mm/yyyy)"
    )
    dt_atendimento: date = Field(
        ..., description="Data de realização do atendimento (formato: dd/mm/yyyy)"
    )
    hr_atendimento: time = Field(
        ..., description="Horário de realização do atendimento (formato: HH:MM)"
    )
    dt_emissao_tiss: date = Field(
        ..., description="Data de emissão da guia no formato TISS (formato: d/mm/yyyy)"
    )
    cd_beneficiario: str = Field(
        ..., description="Código do beneficiário (código do paciente)"
    )
    nm_beneficiario: str | None = Field(
        None, description="Nome do beneficiário (nome do paciente)"
    )
    ds_endereco_beneficiario: str | None = Field(
        None, description="Endereço do beneficiário (endereço do paciente)"
    )
    cd_solicitante: str = Field(
        ...,
        description="Código do solicitante (código do profissional de saúde que solicitou o atendimento)",
    )
    nm_solicitante: str = Field(
        ...,
        description="Nome do solicitante (nome do profissional de saúde que solicitou o atendimento)",
    )
    ds_especialidade: str = Field(
        ..., description="Especialidade do atendimento (ex: Dermatologia, Pediatria)"
    )
    st_atendimento: str = Field(
        ..., description="Status do atendimento (ex: Realizado, Cancelado)"
    )
    tp_atendimento: str = Field(
        ..., description="Tipo do atendimento (ex: Consulta, Exame)"
    )
    fg_retorno: bool = Field(..., description="Indicação de retorno (Sim ou Não)")
    cd_senha_terapia: str | None = Field(
        None, description="Número da senha de terapia, se aplicável"
    )
    cd_procedimento: str = Field(..., description="Código do procedimento realizado")
    ds_procedimento: str = Field(..., description="Nome do procedimento realizado")
    qt_procedimento: int = Field(
        ..., description="Quantidade do procedimento realizado"
    )
    qt_sessoes_executadas: int | None = Field(
        None, description="Número de sessões executadas, se aplicável"
    )
    cd_prestador: str = Field(
        ...,
        description="Código do prestador (código do profissional de saúde que realizou o atendimento)",
    )
    nm_prestador: str = Field(
        ...,
        description="Nome do prestador (nome do profissional de saúde que realizou o atendimento)",
    )
    ds_especialidade_prestador: str = Field(
        ..., description="Especialidade do prestador (ex: Dermatologia, Pediatria)"
    )
    ds_indicacao_clinica: str | None = Field(
        None, description="Indicação clínica para o procedimento realizado"
    )
    st_export: str = Field(
        ..., description="Indica se o atendimento foi exportado no sistema de origem"
    )
    dt_export: date = Field(
        ...,
        description="Data de exportação do atendimento no sistema de origem (formato: dd/mm/yyyy)",
    )
    dt_senha: date = Field(
        ...,
        description="Data de geração da senha de terapia, se aplicável (formato: dd/mm/yyyy)",
    )
    cd_operador_execucao: str = Field(
        ..., description="Código do operador que executou o atendimento, se disponível"
    )
    cd_operador_senha: str | None = Field(
        None, description="Código do operador que gerou a senha, se disponível"
    )
    cd_operador_cancelamento: str | None = Field(
        None, description="Código do operador que cancelou o atendimento, se disponível"
    )
    ds_observacao: str | None = Field(
        None, description="Observações adicionais sobre o atendimento, se disponíveis"
    )
    dt_base: int = Field(..., description="Mês e ano base do arquivo (formato: yyyymm)")
    file_name: str = Field(..., description="Nome do arquivo de origem do atendimento")
