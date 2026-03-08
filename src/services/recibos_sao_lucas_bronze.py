import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core import ReadFile, db, logger, set_default_dt_base, move_file
from src.models import RecibosSaoLucasBronze as RecibosBronzeModel
from src.schemas import ReciboSaoLucasBronzeSchema


class RecibosSaoLucasBronze:
    def __init__(
        self,
        dt_base: int | None = None,
    ) -> None:
        self.recibos_sao_lucas_data_path = "./data/recibos_sao_lucas"
        self.dt_base = set_default_dt_base(dt_base)
        self.landzone_path = f"{self.recibos_sao_lucas_data_path}/landzone/"
        self.processed_path = f"{self.recibos_sao_lucas_data_path}/processed/"
        self.file_name = f"{self.dt_base}_recibos_sao_lucas"

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified file and return it as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the loaded data.
        """
        try:
            df = ReadFile(
                file_path=self.landzone_path,
                file_name=self.file_name,
            ).main()
        except Exception as e:
            logger.error(f"Error loading data for Recibos Sao Lucas Bronze: {e}")
            raise
        else:
            logger.info(
                f"Data loaded successfully for Recibos Sao Lucas Bronze: {self.file_name}"
            )
            return df

    def add_control_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add control columns (dt_base and file_name) to the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to which the control columns will be added.

        Returns:
            pd.DataFrame: The DataFrame with the added control columns.
        """
        try:
            df["dt_base"] = self.dt_base
        except Exception as e:
            logger.error(
                f"Error adding control columns for Recibos Sao Lucas Bronze: {e}"
            )
            raise
        else:
            logger.info(
                f"Columns dt_base and file_name added successfully for Recibos Sao Lucas Bronze: {self.file_name}"
            )
            return df

    def create_invoice_data(self, row: pd.Series) -> ReciboSaoLucasBronzeSchema:
        """
        Create ReciboSaoLucasBronzeSchema object from a row of the DataFrame.

        Args:
            row (pd.Series): A row from the DataFrame.

        Returns:
            ReciboSaoLucasBronzeSchema: The created schema object.
        """
        try:
            invoice_data = ReciboSaoLucasBronzeSchema(
                dt_atendimento=row["dt_atendimento"],
                cd_beneficiario=row["cd_beneficiario"],
                cd_procedimento=row["cd_procedimento"],
                qt_procedimento=row["qt_procedimento"],
                vl_procedimento=row["vl_procedimento"],
                nr_pagina=row["nr_pagina"],
                dt_base=row["dt_base"],
                file_name=row["file_name"]
            )
        except Exception as e:
            logger.error(
                f"Error creating ReciboSaoLucasBronzeSchema object: {e}"
            )
            raise e
        else:
            return invoice_data

    def get_invoice_by_beneficiario_procedimento_atendimento(
        self, session: Session, cd_beneficiario: str, cd_procedimento: str, dt_atendimento: str
    ) -> RecibosBronzeModel | None:
        """
        Retrieve a RecibosSaoLucasBronze record from the database based on beneficiario and procedimento.

        Args:
            session (Session): The database session to use for the query.
            cd_beneficiario (str): The beneficiario code to filter by
            cd_procedimento (str): The procedimento code to filter by.
            dt_atendimento (str): The date of the atendimento to filter by.
        
        Returns:
            RecibosBronzeModel | None: The retrieved record if found, otherwise None.
        """
        try:
            stmt = select(RecibosBronzeModel).where(
                RecibosBronzeModel.cd_beneficiario == cd_beneficiario,
                RecibosBronzeModel.cd_procedimento == cd_procedimento,
                RecibosBronzeModel.dt_atendimento == dt_atendimento
            )
            result = session.execute(stmt).scalar_one_or_none()
        except Exception as e:
            logger.error(
                f"Error retrieving invoice by beneficiario and procedimento: {e} - Beneficiario: {cd_beneficiario}, Procedimento: {cd_procedimento}, Atendimento: {dt_atendimento}"
            )
        else:
            if result:
                logger.info(
                    f"Invoice retrieved successfully for beneficiario: {cd_beneficiario} and procedimento: {cd_procedimento}, Atendimento: {dt_atendimento}"
                )
            else:
                logger.info(
                    f"No invoice found for beneficiario: {cd_beneficiario}, procedimento: {cd_procedimento}, atendimento: {dt_atendimento}"
                )
            return result
        
    def insert_or_update_invoices(
            self, session: Session, invoice_data: ReciboSaoLucasBronzeSchema
        ) -> None:
            """
            Insert or update ReciboSaoLucasBronze records in the session (without committing).

            Args:
                session (Session): The database session to use for the operation.
                invoice_data (ReciboSaoLucasBronzeSchema): The data to insert or update.
            """
            try:
                existing_invoice = self.get_invoice_by_beneficiario_procedimento_atendimento(
                    session, invoice_data.cd_beneficiario, invoice_data.cd_procedimento, invoice_data.dt_atendimento
                )
                if existing_invoice:
                    for field, value in invoice_data.model_dump().items():
                        setattr(existing_invoice, field, value)
                    session.add(existing_invoice)
                    logger.info(
                        f"Invoice updated successfully for beneficiario: {invoice_data.cd_beneficiario} and procedimento: {invoice_data.cd_procedimento}"
                    )
                else:
                    new_invoice = RecibosBronzeModel(**invoice_data.model_dump())
                    session.add(new_invoice)
                    logger.info(
                        f"Invoice inserted successfully for beneficiario: {invoice_data.cd_beneficiario} and procedimento: {invoice_data.cd_procedimento}"
                    )
            except Exception as e:
                logger.error(f"Error inserting or updating invoices: {e}")
                raise

    def main(self) -> bool:
        """
        Main method to run the atendimento sao lucas import pipeline.
        """
        logger.info("RECIBOS SAO LUCAS IMPORT")
        try:
            df = self.load_data()
            df = self.add_control_columns(df)

            num_rows = len(df)
            affected_rows = 0

            with db.session_factory() as session:
                try:
                    for _, row in df.iterrows():
                        service_data = self.create_invoice_data(row)
                        self.insert_or_update_invoices(session, service_data)
                        affected_rows += 1
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

            logger.info(f"Total rows processed: {num_rows}")
            logger.info(f"Total affected rows: {affected_rows}")

            move_file(self.landzone_path, self.file_name, self.processed_path)
        except Exception as e:
            logger.error(f"Error in Recibos Sao Lucas import pipeline: {e}")
            return False
        else:
            logger.info("IMPORT RECIBOS SAO LUCAS COMPLETED SUCCESSFULLY!")
            return True