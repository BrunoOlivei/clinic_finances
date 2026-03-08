from datetime import datetime

from pydantic import BaseModel, Field


class ReciboSaoLucasBronzeSchema(BaseModel):
    dt_atendimento: str = Field(
        ..., description="Data de realização do atendimento (formato: dd/mm/yyyy)"
    )
    cd_beneficiario: str = Field(
        ..., description="Código do beneficiário (código do paciente)"
    )
    cd_procedimento: str = Field(
        ..., description="Código do procedimento realizado"
    )
    qt_procedimento: str = Field(
        ..., description="Quantidade do procedimento realizado"
    )
    vl_procedimento: str = Field(
        ..., description="Valor do procedimento realizado"
    )
    nr_pagina: str = Field(
        ..., description="Número da página do relatório de recibos onde o procedimento está descrito"
    )
    dt_base: int = Field(
        ..., description="Mês e ano base do arquivo no formato YYYYMM (ex: 202401)"
    )
    file_name: str = Field(
        ..., description="Nome do arquivo de origem do recibo"
    )
    silver_exported: bool = Field(
        False, description="Indica se o atendimento foi exportado para a camada silver"
    )
    silver_date_export: datetime | None = Field(
        None,
        description="Data e hora de exportação para a camada silver, se aplicável)",
    )