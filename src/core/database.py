from collections.abc import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.settings import settings


class Database:
    _instance: "Database | None" = None
    _engine: Engine | None = None
    _session_factory: sessionmaker[Session] | None = None

    def __new__(cls) -> "Database":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._engine = create_engine(settings.database_url, echo=False)
            cls._session_factory = sessionmaker(
                bind=cls._engine, autocommit=False, autoflush=False
            )
        return cls._instance

    @property
    def engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine instance.
        """
        return self._engine

    @property
    def session_factory(self) -> sessionmaker[Session]:
        """
        Returns the SQLAlchemy session factory.
        """
        return self._session_factory

    def get_session(self) -> Generator[Session, None, None]:
        """
        Yields a database session and closes it after use.
        """
        session = self._session_factory()
        try:
            yield session
        finally:
            session.close()


db = Database()
