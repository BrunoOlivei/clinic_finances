from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class InsuranceClaimBase(BaseModel):
    id_claim: str
    nr_claim: str
    nr_request: str | None = None
    cd_patient: str
    dt_issue: date
    dm_service: datetime
    st_claim: str
    tp_claim: str
    fg_return: bool
    cd_procedure: str
    nm_procedure: str
    qt_procedure: int


class InsuranceClaimCreate(InsuranceClaimBase):
    pass


class InsuranceClaimUpdate(BaseModel):
    nr_request: str | None = None
    dt_issue: date | None = None
    dm_service: datetime | None = None
    st_claim: str | None = None
    tp_claim: str | None = None
    fg_return: bool | None = None
    cd_procedure: str | None = None
    nm_procedure: str | None = None
    qt_procedure: int | None = None


class InsuranceClaimResponse(InsuranceClaimBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
