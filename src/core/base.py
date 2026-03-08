from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata_obj = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})


class Base(DeclarativeBase):
    metadata = metadata_obj


class BronzeBase(Base):
    __abstract__ = True
    __table_args__ = {
        "schema": "brz",
        "comment": "Tabela base para dados importados na camada bronze",
    }


class SilverBase(Base):
    __abstract__ = True
    __table_args__ = {
        "schema": "slv",
        "comment": "Tabela base para dados processados na camada silver",
    }


class GoldBase(Base):
    __abstract__ = True
    __table_args__ = {
        "schema": "gld",
        "comment": "Tabela base para dados importados na camada gold",
    }
