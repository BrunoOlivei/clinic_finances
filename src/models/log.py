from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UUID, text
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from src.core.base import Base


class Log(Base):
    __tablename__ = "tb_logs"
    __table_args__ = {
        "schema": "log",
        "comment": "Tabela de logs da aplicação",
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Identificador único do log (UUID)",
    )
    level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Nível do log (ex: WARNING, ERROR, CRITICAL)",
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Mensagem do log",
    )
    module: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Módulo onde o log foi gerado",
    )
    function: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Função onde o log foi gerado",
    )
    line: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment="Linha do código onde o log foi gerado",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="Data e hora de criação do log",
    )
