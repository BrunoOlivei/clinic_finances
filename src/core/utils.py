from datetime import datetime

from src.core.logger import logger


def set_default_dt_base(dt_base: int | None) -> int:
    """
    Retorna dt_base no formato YYYYMM. Se não fornecido, usa o mês anterior ao atual.

    Args:
        dt_base: Mês e ano base (formato: yyyymm). None para usar o mês anterior.

    Returns:
        int: Mês e ano base no formato YYYYMM.
    """
    try:
        if dt_base is None:
            now = datetime.now()
            month = now.month - 1 if now.month > 1 else 12
            year = now.year if now.month > 1 else now.year - 1
            dt_base = int(f"{year}{month:02d}")
    except Exception as e:
        logger.error(f"Erro ao definir dt_base: {e}")
        raise
    else:
        logger.info(f"dt_base definido: {dt_base}")
        return dt_base
