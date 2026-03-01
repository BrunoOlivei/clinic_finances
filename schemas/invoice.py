from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class InvoiceBase(BaseModel):
    dt_service: datetime
    cd_patient: str
    cd_procedure: str
    qt_procedure: int
    vl_procedure: Decimal
    nr_page: int
    dt_base: int
    nm_file: str


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    dt_service: datetime | None = None
    cd_patient: str | None = None
    cd_procedure: str | None = None
    qt_procedure: int | None = None
    vl_procedure: Decimal | None = None
    nr_page: int | None = None
    dt_base: int | None = None
    nm_file: str | None = None


class InvoiceResponse(InvoiceBase):
    model_config = ConfigDict(from_attributes=True)

    id_invoice: str
    created_at: datetime
    updated_at: datetime