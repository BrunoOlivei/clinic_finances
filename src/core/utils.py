import os

from datetime import datetime
from typing import Dict
from decimal import Decimal

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
        elif properties["type"] == "decimal":
            df[column] = df[column].apply(
                lambda x: Decimal(str(x).replace(",", ".")) if pd.notnull(x) else None
            )
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


def move_file(landzone_path: str, file_name: str, processed_path: str) -> None:
    """
    Move the processed file from the landzone directory to the processed directory.

    Args:
        landzone_path (str): The origin path of the file.
        file_name (str): The file name.
        processed_path (str): The destination path of the file.
    """
    try:
        files = os.listdir(landzone_path)
        for file in files:
            if os.path.splitext(file.lower())[0] == file_name:
                source_file = os.path.join(landzone_path, file)
                destination_file = os.path.join(processed_path, file)
                os.rename(source_file, destination_file)
                logger.info(
                    f"File moved successfully from {source_file} to {destination_file}"
                )
    except Exception as e:
        logger.error(
            f"Error moving file from {source_file} to {destination_file}: {e}"
        )
        raise