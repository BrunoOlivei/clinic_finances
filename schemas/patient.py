from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    cd_patient: str
    nm_patient: str
    ds_address: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    nm_patient: str | None = None
    ds_address: str | None = None


class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
