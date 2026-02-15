from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Log(Base):
    __tablename__ = "logs"
    __table_args__ = {
        "comment": "Registro de logs da aplicação capturados pelo Loguru",
    }

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do registro de log",
    )
    level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="Nível de severidade do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Mensagem descritiva do evento registrado",
    )
    module: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        comment="Nome do módulo Python que originou o log",
    )
    function: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        comment="Nome da função que originou o log",
    )
    line: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Número da linha no código fonte que originou o log",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="Data e hora em que o log foi registrado",
    )

    def __repr__(self) -> str:
        return f"<Log(id={self.id}, level='{self.level}', message='{self.message[:50]}')>"
