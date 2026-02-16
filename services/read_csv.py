from datetime import datetime
from pathlib import Path

import pandas as pd

from core import logger


class ReadCSV:
    def __init__(
        self,
        data_dir: str = "./data",
        file_pattern: str = "{year}{month:02d}_atendimentos_sao_lucas.csv",
    ) -> None:
        self.data_dir = Path(data_dir)
        self.file_pattern = file_pattern

    def get_csv_path(
        self, year: int | None = None, month: int | None = None
    ) -> Path:
        """
        Builds the CSV file path for the given year and month.

        Args:
            year (int | None, optional): The year for the CSV file. Defaults to current year.
            month (int | None, optional): The month for the CSV file. Defaults to current month.

        Returns:
            Path: The path to the CSV file.
        """
        now = datetime.now()
        year = year or now.year
        month = month or now.month

        filename = self.file_pattern.format(year=year, month=month)
        return self.data_dir / filename

    def read(self, year: int | None = None, month: int | None = None) -> pd.DataFrame:
        """
        Reads the CSV file for the given year/month and returns a DataFrame.

        Args:
            year (int | None, optional): The year for the CSV file. Defaults to current year.
            month (int | None, optional): The month for the CSV file. Defaults to current month.

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """
        csv_path = self.get_csv_path(year, month)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        try:
            logger.info(f"Reading CSV file: {csv_path}")
            return pd.read_csv(csv_path, encoding="utf-8-sig", dtype=str)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise
