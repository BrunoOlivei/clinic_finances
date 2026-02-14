from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cd_patient: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, index=True
    )
    nm_patient: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    ds_address: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, cd_patient='{self.cd_patient}', nm_patient='{self.nm_patient}')>"
