from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cd_patiente: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    nm_patiente: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    ds_endereco: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, cd_patiente='{self.cd_patiente}', nm_patiente='{self.nm_patiente}')>"
