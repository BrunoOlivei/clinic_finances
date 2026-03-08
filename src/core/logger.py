import sys

from loguru import logger


def _db_sink(message):
    """Sink that persists WARNING+ logs to the database."""
    record = message.record

    from src.models.log import Log

    from src.core.database import db

    session = db.session_factory()
    try:
        log_entry = Log(
            level=record["level"].name,
            message=str(record["message"]),
            module=record["module"],
            function=record["function"],
            line=record["line"],
        )
        session.add(log_entry)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def setup_logger():
    """Configure loguru with console, file, and database sinks."""
    logger.remove()

    # Console sink — INFO+, colored
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — "
        "<level>{message}</level>",
        colorize=True,
    )

    # File sink — DEBUG+, daily rotation
    logger.add(
        "logs/{time:YYYY-MM-DD}.log",
        level="DEBUG",
        rotation="1 day",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
        "{module}:{function}:{line} — {message}",
        encoding="utf-8",
    )

    # Database sink — WARNING+
    logger.add(
        _db_sink,
        level="WARNING",
        format="{message}",
    )

    return logger


logger = setup_logger()  # noqa: F811
