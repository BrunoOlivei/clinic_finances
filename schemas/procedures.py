from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProcedureBase(BaseModel):
    cd_procedure: str
    nm_procedure: str
    vl_procedure: float


class ProcedureCreate(ProcedureBase):
    pass


class ProcedureResponse(ProcedureBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime