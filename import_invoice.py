from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import List

import pandas as pd

from core import db, logger
from schemas import InvoiceCreate, InvoiceUpdate
from services import InvoiceService


class IngestInvoiceData:
    def __init__(
        self,
        year: int | None = None,
        month: int | None = None,
        data_dir: str = "./data",
        file_pattern: str = "{year}{month:02d}_recibo_sao_lucas.csv",
    ) -> None:
        self.year = year
        self.month = month
        self.file_pattern = file_pattern
        self.data_dir = data_dir

    def set_default_year_month(self) -> None:
        """
        Set default values for year and month if they are not provided.
        Defaults to the previous month of the current year.
        """
        now = datetime.now()
        if self.year is None or self.month is None:
            previous_month = now.month - 1 if now.month > 1 else 12
            previous_year = now.year if now.month > 1 else now.year - 1
            self.year = self.year or previous_year
            self.month = self.month or previous_month

    def set_file_name(self) -> str:
        """
        Set the file name based on the year and month.

        Returns:
            str: The file name for the CSV file.
        """
        self.set_default_year_month()
        return self.file_pattern.format(year=self.year, month=self.month)

    def set_csv_path(self) -> str:
        """
        Set the full path to the CSV file.

        Returns:
            str: The full path to the CSV file.
        """
        file_name = self.set_file_name()
        return str(Path(self.data_dir) / file_name)

    def read_csv(self) -> pd.DataFrame:
        """
        Read the CSV file and return a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.
        """
        csv_path = self.set_csv_path()
        try:
            logger.info(f"Reading CSV file: {csv_path}")
            return pd.read_csv(csv_path, encoding="utf", dtype=str, sep=";")
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise

    def transform_dt_service(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the dt_service string to the desired format.

        Args:
            df (pd.DataFrame): The DataFrame containing the dt_service column.


        Returns:
            pd.DataFrame: The DataFrame with the transformed dt_service column.
        """
        try:
            df["dt_service"] = df[["dt_service"]].apply(
                lambda x: pd.to_datetime(
                    x, format="%d/%m/%Y", errors="coerce", dayfirst=True
                )
            )
            return df
        except Exception as e:
            logger.error(f"Error transforming dt_service: {e}")
            raise

    def create_invoice_data(self, row: pd.Series) -> InvoiceCreate:
        """
        Create an InvoiceCreate object from the extracted data.

        Args:
            row (pd.Series): The extracted data to create the InvoiceCreate object from.

        Returns:
            InvoiceCreate: The created InvoiceCreate object.
        """
        try:
            return InvoiceCreate(
                cd_patient=row["cd_patient"],
                cd_procedure=row["cd_procedure"],
                dt_service=row["dt_service"],
                qt_procedure=row["qt_procedure"],
                vl_procedure=Decimal(row["vl_procedure"]),
                nr_page=row["nr_page"],
                dt_base=row["dt_base"],
                nm_file=row["nm_file"],
            )
        except Exception as e:
            logger.error(f"Error creating InvoiceCreate object: {e}")
            raise

    def insert_or_update_invoices(
        self, service: InvoiceService, invoices_data: List[InvoiceCreate]
    ) -> None:
        inserted_num = 0
        updated_num = 0
        try:
            for invoice_data in invoices_data:
                existing_invoice = service.get_by_cd_patient_cd_procedure(
                    invoice_data.cd_patient,
                    invoice_data.cd_procedure,
                    invoice_data.dt_service,
                )
                if existing_invoice:
                    logger.info(
                        f"Updating existing invoice: {existing_invoice.id_invoice}"
                    )
                    service.update(
                        existing_invoice.id_invoice,
                        InvoiceUpdate(**invoice_data.model_dump()),
                    )
                    updated_num += 1
                else:
                    logger.info(
                        f"Inserting new invoice for patient {invoice_data.cd_patient} and procedure {invoice_data.cd_procedure}"
                    )
                    service.create(invoice_data)
                    inserted_num += 1
            logger.info(f"Inserted {inserted_num} new invoices")
            logger.info(f"Updated {updated_num} existing invoices")
        except Exception as e:
            logger.error(f"Error inserting or updating invoices: {e}")
            raise

    def run(self, year: int | None = None, month: int | None = None) -> None:
        """
        Run the data ingestion process for the specified year and month.

        Args:
            year (int | None): The year of the invoice data to ingest. If None, defaults to the previous month.
            month (int | None): The month of the invoice data to ingest. If None, defaults to the previous month.
        """
        logger.info("INVOICE DATA INGESTION STARTED")

        invoice_data = self.read_csv()
        invoice_data = self.transform_dt_service(invoice_data)

        invoices_create = []

        for _, row in invoice_data.iterrows():
            invoices_create.append(self.create_invoice_data(row))

        with db.session_factory() as session:
            invoice_service = InvoiceService(session)
            self.insert_or_update_invoices(invoice_service, invoices_create)

            total_invoices = invoice_service.count()
            logger.info(f"Total invoices in the database: {total_invoices}")

        logger.success("INVOICE DATA INGESTION COMPLETED SUCCESSFULLY")


# %%
if __name__ == "__main__":
    IngestInvoiceData(year=2026, month=1).run()
