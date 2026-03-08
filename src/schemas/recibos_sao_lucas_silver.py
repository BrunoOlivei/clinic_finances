from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class ReciboSaoLucasSilverSchema(BaseModel):
    dt_atendimento: date = Field(..., description="Data de realização do atendimento")
    cd_beneficiario: str = Field(
        ..., description="Código do beneficiário (código do paciente)"
    )
    cd_procedimento: str = Field(..., description="Código do procedimento realizado")
    qt_procedimento: int = Field(
        ..., description="Quantidade do procedimento realizado"
    )
    vl_procedimento: Decimal = Field(..., description="Valor do procedimento realizado")
    nr_pagina: int = Field(
        ...,
        description="Número da página do relatório de atendimento onde o procedimento está descrito",
    )
    dt_base: int = Field(
        ..., description="Mês e ano base do arquivo no formato YYYYMM (ex: 202401)"
    )
    file_name: str = Field(..., description="Nome do arquivo de origem do registro")
