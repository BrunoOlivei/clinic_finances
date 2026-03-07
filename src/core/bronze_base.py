from core.base import Base

class BronzeBase(Base):
    __abstract__ = True
    __table_args__ = {
        "schema": "brz",
        "comment": "Tabela base para dados importados na camada bronze"
    }