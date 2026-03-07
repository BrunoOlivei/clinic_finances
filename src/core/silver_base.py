from core.base import Base

class SilverBase(Base):
    __abstract__ = True
    __table_args__ = {
        "schema": "slv",
        "comment": "Tabela base para dados processados na camada silver"
    }