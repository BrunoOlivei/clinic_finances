from core.base import Base

class GoldBase(Base):
    __abstract__ = True
    __table_args__ = {
        "schema": "gld",
        "comment": "Tabela base para dados importados na camada gold"
    }