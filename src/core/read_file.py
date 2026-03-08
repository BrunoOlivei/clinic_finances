import os
import re
from csv import Sniffer
from pathlib import Path
from typing import Optional

import chardet
import unicodedata
import pandas as pd
from pandas import errors as pd_errors

from src.core import logger


class ReadFile:
    def __init__(
        self, file_path: str, file_name: str, sheet_name: Optional[str] = None
    ) -> None:
        self.file_path = file_path
        self.file_name = file_name
        self.sheet_name = sheet_name

    @staticmethod
    def _format_path(file_path: str) -> str:
        """
        Format the file path to lowercase.

        Args:
            file_path (str): The file path to format.

        Raises:
            ValueError: If the file path is not a string.

        Returns:
            str: The formatted file path.
        """
        try:
            return file_path.lower()
        except AttributeError:
            raise ValueError("The path must be a string.")

    @staticmethod
    def _validate_directory(file_path: str) -> bool:
        """
        Validate if the provided file path is a directory.

        Args:
            file_path (str): The file path to validate.

        Raises:
            NotADirectoryError: If the provided file path is not a valid directory.

        Returns:
            bool: True if the file path is a valid directory, otherwise raises an error.
        """
        if not os.path.isdir(file_path):
            raise NotADirectoryError(f"The path {file_path} is not a valid directory.")
        return True

    @staticmethod
    def _find_file_in_directory(file_path: str, file_name: str) -> str:
        """
        Search for a file in the specified directory that matches the given file name (case-insensitive).

        Args:
            file_path (str): The directory path to search for the file.
            file_name (str): The name of the file to search for (case-insensitive).

        Raises:
            FileNotFoundError: If the file is not found in the directory.
            e: If an unexpected error occurs during the file search.

        Returns:
            str: The name of the found file.
        """
        try:
            files = os.listdir(file_path)
            for file in files:
                if os.path.splitext(file.lower())[0] == file_name.lower():
                    return file
            raise FileNotFoundError(
                f"The file {file_name} was not found in the directory {file_path}."
            )
        except FileNotFoundError as e:
            raise e

    def _set_full_path(self, file_path: str, file_name: str) -> Path:
        """
        Set the full path of the file by combining the directory path and the file name.

        Args:
            file_path (str): The directory path where the file is located.
            file_name (str): The name of the file to find in the directory.

        Raises:
            e: If an error occurs during the process of setting the full file path.

        Returns:
            Path: The full path of the file as a Path object.
        """
        try:
            path_formatted = self._format_path(file_path)
            if self._validate_directory(path_formatted):
                file_name_found = self._find_file_in_directory(
                    path_formatted, file_name
                )
                full_file_path = os.path.join(path_formatted, file_name_found)
                return Path(full_file_path)
        except Exception as e:
            raise e

    @staticmethod
    def _get_file_extension(file_name_target: str) -> str:
        """
        Get the file extension from the given file name.

        Args:
            file_name_target (str): The name of the file to extract the extension from.

        Raises:
            ValueError: If the file name does not contain an extension.

        Returns:
            str: The file extension.
        """
        try:
            return file_name_target.split(".")[-1]
        except IndexError:
            raise ValueError("The file name must contain an extension.")

    @staticmethod
    def _detect_encoding(full_file_path: str) -> str:
        """
        Detect the encoding of the given file.

        Args:
            full_file_path (str): The full path of the file to detect the encoding.

        Raises:
            Exception: If an error occurs during the encoding detection.

        Returns:
            str: The detected encoding of the file.
        """
        try:
            with open(full_file_path, "rb") as f:
                raw_data = f.read(10000)
            result = chardet.detect(raw_data)

            if result["encoding"] == "UTF-8-SIG":
                return "utf-8"
            return result["encoding"] or "utf-8"
        except Exception as e:
            raise Exception(f"Error detecting file encoding: {e}")

    @staticmethod
    def _detect_delimiter(full_file_path: str, encoding: str) -> str:
        """
        Detect the delimiter used in the given CSV file.

        Args:
            full_file_path (str): The full path of the CSV file to detect the delimiter.
            encoding (str): The encoding of the CSV file.

        Raises:
            ValueError: If the detected delimiter is not supported.
            Exception: If an error occurs during the delimiter detection.

        Returns:
            str: The detected delimiter.
        """
        try:
            sniffer = Sniffer()
            with open(full_file_path, "r", encoding=encoding) as f:
                sample = f.read(10000)
                result = sniffer.sniff(sample)
                delimiter = result.delimiter
            if delimiter in [";", ",", "\t", "|"]:
                return delimiter
            else:
                raise ValueError(f"Detected delimiter '{delimiter}' is not supported.")
        except Exception as e:
            raise Exception(f"Error detecting file delimiter: {e}")

    @staticmethod
    def _read_csv(full_file_path: Path, encoding: str, delimiter: str) -> pd.DataFrame:
        """
        Read a CSV file and return its contents as a pandas DataFrame.

        Args:
            full_file_path (Path): The full path of the CSV file to read.
            encoding (str): The encoding of the CSV file.
            delimiter (str): The delimiter used in the CSV file.

        Raises:
            ValueError: If the CSV file is empty or if there is an error parsing the CSV file.
            Exception: If an error occurs while reading the CSV file.

        Returns:
            pd.DataFrame: The contents of the CSV file as a pandas DataFrame.
        """
        try:
            df = pd.read_csv(
                full_file_path, encoding=encoding, delimiter=delimiter, dtype=str
            )
            return df
        except pd_errors.EmptyDataError:
            raise ValueError("The CSV file is empty.")
        except pd_errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {e}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")

    @staticmethod
    def read_excel(full_file_path: Path, sheet_name: str) -> pd.DataFrame:
        """
        Read an Excel file and return its contents as a pandas DataFrame.

        Args:
            full_file_path (Path): The full path of the Excel file to read.
            sheet_name (str): The name of the sheet to read.

        Raises:
            ValueError: If the Excel file is empty or if there is an error parsing the Excel file.
            Exception: If an error occurs while reading the Excel file.

        Returns:
            pd.DataFrame: The contents of the Excel file as a pandas DataFrame.
        """
        try:
            df = pd.read_excel(
                full_file_path, sheet_name=sheet_name, dtype=str, engine="openpyxl"
            )
            return df
        except pd_errors.EmptyDataError:
            raise ValueError("The Excel file is empty.")
        except pd_errors.ParserError as e:
            raise ValueError(f"Error parsing Excel file: {e}")
        except Exception as e:
            raise Exception(f"Error reading Excel file: {e}")

    def load_data(self) -> pd.DataFrame:
        """
        Load data from a specified file path and file name, and return it as a pandas DataFrame.

        Raises:
            ValueError: If there is an error loading the data.
            ValueError: If the file extension is not supported.
            Exception: If an unexpected error occurs while loading the data.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        try:
            logger.info(
                f"Loading data from path: {self.file_path}, file: {self.file_name}"
            )
            full_file_path = self._set_full_path(self.file_path, self.file_name)
            extension = self._get_file_extension(full_file_path.name)

            if extension in ["csv"]:
                encoding = self._detect_encoding(full_file_path)
                delimiter = self._detect_delimiter(full_file_path, encoding)
                df = self._read_csv(full_file_path, encoding, delimiter)
                logger.info(f"Successfully loaded CSV file: {full_file_path}")
                return df
            elif extension in ["xlsx", "xls"]:
                if not self.sheet_name:
                    logger.error("Sheet name must be provided for Excel files.")
                    raise ValueError("Sheet name must be provided for Excel files.")
                df = self.read_excel(full_file_path, self.sheet_name)
                logger.info(f"Successfully loaded Excel file: {full_file_path}")
                return df
            else:
                logger.error(f"Unsupported file extension: {extension}")
                raise ValueError(f"Unsupported file extension: {extension}")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise e

    def column_sanitizer(self, column_name: str) -> str:
        """
        Sanitize column name changing it to lower casa, removing the accents and replacing especial characteres to underscore

        Args:
            column_name (str): the column name to be sanitize

        Return:
            str: the column name sanitized
        """
        try:
            normalized = unicodedata.normalize("NFD", column_name)
            without_accents = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
            lowered = without_accents.lower()
            sanitized = re.sub(r"[^a-z0-9]+", "_", lowered)
            column_sanitized = sanitized.strip("_")
        except Exception as e:
            logger.error(f"Error sanitizing column: {column_name}, error: {e}")
            raise
        else:
            return column_sanitized
        

    def sanitize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            for column in df.columns:
                sanitized_column = self.column_sanitizer(column)
                df.rename(columns={column: sanitized_column}, inplace=True)
        except Exception as e:
            logger.error(f"Error sanitizing columns: {e}")     
            raise
        else:
            logger.info("Columns sanitized successfuly")
            return df

    def main(self) -> pd.DataFrame:
        try:
            df = self.load_data()
            df_sanitized = self.sanitize_columns(df)
        except Exception as e:
            logger.error(f"Error in ReadFile main method: {e}")
            raise
        else:
            logger.info("Data loaded and sanitized successfully")
            return df_sanitized