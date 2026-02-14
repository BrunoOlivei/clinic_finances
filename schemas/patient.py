from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    cd_patiente: str
    nm_patiente: str
    ds_endereco: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    nm_patiente: str | None = None
    ds_endereco: str | None = None


class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
