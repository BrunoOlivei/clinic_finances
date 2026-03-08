from datetime import datetime
from typing import Dict

import pandas as pd

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


def format_type_data(df: pd.DataFrame, schema: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """
    Format the data types of the DataFrame columns according to the defined schema.

    Args:
        df (pd.DataFrame): The DataFrame to be formatted.
        schema (Dict[str, Dict[str, str]]): 

    Returns:
        pd.DataFrame: The DataFrame with formatted data types.
    """
    for column, properties in schema.items():
        if column not in df.columns:
            continue
        if properties["type"] == "date":
            df[column] = pd.to_datetime(
                df[column],
                format=properties["format"],
                errors="coerce",
                dayfirst=True,
            ).dt.date
        elif properties["type"] == "time":
            df[column] = pd.to_datetime(
                df[column], format=properties["format"], errors="coerce"
            ).dt.time
        elif properties["type"] == "datetime":
            df[column] = pd.to_datetime(
                df[column], format=properties["format"], errors="coerce", dayfirst=True
            )
        elif properties["type"] == "integer":
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
        elif properties["type"] == "string":
            df[column] = df[column].str.strip().astype(str)
        elif properties["type"] == "boolean":
            df[column] = df[column].apply(
                lambda x: True if x.lower() in ["true", "1", "yes", "sim"] else False
            )
        else:
            raise ValueError(
                "Error formating type of columns data"
            )
            
    return df