import pandas as pd
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core import db, format_type_data, logger, set_default_dt_base
from src.models import RecibosSaoLucasBronze as RecibosBronzeModel
from src.models import RecibosSaoLucasSilver as RecibosSilverModel
from src.schemas import ReciboSaoLucasSilverSchema


class RecibosSaoLucasSilver:
    def __init__(
        self,
        dt_base: int | None = None,
    ) -> None:
        self.dt_base = set_default_dt_base(dt_base)
        self.file_name = f"98663RELATORIO_ATENDIMENTO_{str(self.dt_base)[-2:]}_{str(self.dt_base)[:4]}.pdf"
        self.schema = {
            "dt_atendimento": {
                "type": "date",
                "format": "%d/%m/%Y",
            },
            "cd_beneficiario": {"type": "string"},
            "cd_procedimento": {"type": "string"},
            "qt_procedimento": {"type": "integer"},
            "vl_procedimento": {"type": "decimal"},
            "nr_pagina": {"type": "integer"},
        }

    def load_data(self, session: Session) -> pd.DataFrame:
        """
        Load unprocessed records from the bronze table.

        Args:
            session (Session): The database session to use for the query.

        Returns:
            pd.DataFrame: The DataFrame containing the loaded data.
        """
        try:
            stmt = select(RecibosBronzeModel).where(
                RecibosBronzeModel.file_name == self.file_name,
                RecibosBronzeModel.silver_exported == False,  # noqa: E712
            )
            df = pd.read_sql_query(stmt, session.connection())
        except Exception as e:
            logger.error(f"Error loading data for Recibos Sao Lucas Bronze: {e}")
            raise
        else:
            logger.info(
                f"Data loaded successfully for Recibos Sao Lucas Bronze: {self.file_name}"
            )
            return df

    def create_invoice_data(self, row: pd.Series) -> ReciboSaoLucasSilverSchema:
        """
        Create a ReciboSaoLucasSilverSchema instance from a row of the DataFrame.

        Args:
            row (pd.Series): A row of the DataFrame containing the data.

        Returns:
            ReciboSaoLucasSilverSchema: The created schema object.
        """
        try:
            invoice_data = ReciboSaoLucasSilverSchema(
                dt_atendimento=row["dt_atendimento"],
                cd_beneficiario=row["cd_beneficiario"],
                cd_procedimento=row["cd_procedimento"],
                qt_procedimento=row["qt_procedimento"],
                vl_procedimento=row["vl_procedimento"],
                nr_pagina=row["nr_pagina"],
                dt_base=row["dt_base"],
                file_name=row["file_name"],
            )
        except Exception as e:
            logger.error(
                f"Error creating invoice data for Recibos Sao Lucas Silver: {e}"
            )
            raise
        else:
            return invoice_data

    def get_invoice_by_beneficiario_procedimento_atendimento(
        self, session: Session, cd_beneficiario: str, cd_procedimento: str, dt_atendimento: date
    ) -> RecibosSilverModel | None:
        """
        Retrieve an invoice from the silver table based on the beneficiary code, procedure code, and atendimento date.

        Args:
            session (Session): The database session to use for the query.
            cd_beneficiario (str): The beneficiary code to filter by.
            cd_procedimento (str): The procedure code to filter by.
            dt_atendimento (date): The date of the atendimento to filter by.

        Returns:
            RecibosSilverModel | None: The retrieved invoice object if found, otherwise None.
        """
        try:
            stmt = select(RecibosSilverModel).where(
                RecibosSilverModel.cd_beneficiario == cd_beneficiario,
                RecibosSilverModel.cd_procedimento == cd_procedimento,
                RecibosSilverModel.dt_atendimento == dt_atendimento,
            )
            result = session.execute(stmt).scalar_one_or_none()
            return result
        except Exception as e:
            logger.error(
                f"Error retrieving invoice by beneficiary {cd_beneficiario}, procedure {cd_procedimento} and atendimento {dt_atendimento}: {e}"
            )
            raise
        else:
            if result:
                logger.info(
                    f"Invoice retrieved successfully for beneficiary {cd_beneficiario}, procedure {cd_procedimento} and atendimento {dt_atendimento}"
                )
            else:
                logger.info(
                    f"No invoice found for beneficiary {cd_beneficiario}, procedure {cd_procedimento} and atendimento {dt_atendimento}"
                )
            return result

    def insert_or_update_invoices(
        self, session: Session, invoice_data: ReciboSaoLucasSilverSchema
    ) -> None:
        """
        Insert a new invoice into the silver table or update an existing one based on the beneficiary code and procedure code.

        Args:
            session (Session): The database session to use for the operation.
            invoice_data (ReciboSaoLucasSilverSchema): The invoice data to be inserted
        """
        try:
            existing_invoice = self.get_invoice_by_beneficiario_procedimento_atendimento(
                session, invoice_data.cd_beneficiario, invoice_data.cd_procedimento, invoice_data.dt_atendimento
            )
            if existing_invoice:
                for field, value in invoice_data.dict().items():
                    setattr(existing_invoice, field, value)
                session.add(existing_invoice)
                logger.info(
                    f"Invoice updated successfully for beneficiary {invoice_data.cd_beneficiario} and procedure {invoice_data.cd_procedimento}"
                )
            else:
                new_invoice = RecibosSilverModel(**invoice_data.dict())
                session.add(new_invoice)
                logger.info(
                    f"Invoice inserted successfully for beneficiary {invoice_data.cd_beneficiario} and procedure {invoice_data.cd_procedimento}"
                )
        except Exception as e:
            logger.error(f"Error inserting or updating invoice: {e}")
            raise

    def main(self) -> bool:
        """
        Main method to run the recibos sao lucas silver import pipeline.
        """
        logger.info("RECIBOS SAO LUCAS SILVER IMPORT")
        try:
            with next(db.get_session()) as session:
                df = self.load_data(session)
                df = format_type_data(df, self.schema)

                num_rows = len(df)
                affected_rows = 0

                try:
                    for _, row in df.iterrows():
                        invoice_data = self.create_invoice_data(row)
                        self.insert_or_update_invoices(session, invoice_data)
                        affected_rows += 1
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

            logger.info(f"Total rows processed: {num_rows}")
            logger.info(f"Total affected rows: {affected_rows}")
        except Exception as e:
            logger.error(f"Error in Recibos Sao Lucas Silver pipeline: {e}")
            return False
        else:
            logger.info("IMPORT RECIBOS SAO LUCAS SILVER COMPLETED SUCCESSFULLY!")
            return True
