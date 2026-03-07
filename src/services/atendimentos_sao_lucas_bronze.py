import os

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core import ReadFile, db, logger, set_default_dt_base
from src.models import AtendimentosSaoLucasBronze as AtendimentosBronzeModel
from src.schemas import AtendimentoSaoLucasBronzeSchema


class AtendimentosSaoLucasBronze:
    def __init__(
        self,
        dt_base: int | None = None,
    ) -> None:
        self.atendimentos_sao_lucas_data_path = "./data/atendimentos_sao_lucas"
        self.dt_base = set_default_dt_base(dt_base)
        self.landzone_path = f"{self.atendimentos_sao_lucas_data_path}/landzone/"
        self.processed_path = f"{self.atendimentos_sao_lucas_data_path}/processed/"
        self.file_name = f"{self.dt_base}_atendimentos_sao_lucas"

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
            logger.error(f"Error loading data for Atendimentos Sao Lucas Bronze: {e}")
            raise
        else:
            logger.info(
                f"Data loaded successfully for Atendimentos Sao Lucas Bronze: {self.file_name}"
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
            df["file_name"] = self.file_name
        except Exception as e:
            logger.error(
                f"Error adding control columns for Atendimentos Sao Lucas Bronze: {e}"
            )
            raise
        else:
            logger.info(
                f"Columns dt_base and file_name added successfully for Atendimentos Sao Lucas Bronze: {self.file_name}"
            )
            return df

    def create_service_data(self, row: pd.Series) -> AtendimentoSaoLucasBronzeSchema:
        """
        Create an AtendimentoSaoLucasBronzeSchema object from a row of the DataFrame.

        Args:
            row (pd.Series): A row from the DataFrame.

        Returns:
            AtendimentoSaoLucasBronzeSchema: The created schema object.
        """
        try:
            service_data = AtendimentoSaoLucasBronzeSchema(
                terminal=row["terminal"],
                guia=row["guia"],
                emissao=row["emissao"],
                atendimento=row["atendimento"],
                horario=row["horario"],
                emissao_tiss=row["emissao_tiss"],
                cd_beneficiario=row["cd_beneficiario"],
                beneficiario=row["beneficiario"]
                if not pd.isna(row["beneficiario"])
                else None,
                endereco_beneficiario=row["endereco_beneficiario"]
                if not pd.isna(row["endereco_beneficiario"])
                else None,
                solicitante=row["solicitante"],
                solicitante_1=row["solicitante_1"],
                especialidade=row["especialidade"],
                status=row["status"],
                tipo=row["tipo"],
                retorno=row["retorno"],
                senha_terapia=row["senha_terapia"]
                if not pd.isna(row["senha_terapia"])
                else None,
                procedimento=row["procedimento"],
                procedimento_1=row["procedimento_1"],
                quantidade=row["quantidade"],
                sessoes_executadas=row["sessoes_executadas"],
                prestador=row["prestador"],
                prestador_1=row["prestador_1"],
                especialidade_1=row["especialidade_1"],
                indicacao_clinica=row["indicacao_clinica"]
                if not pd.isna(row["indicacao_clinica"])
                else None,
                status_export=row["status_export"],
                dt_export=row["dt_export"],
                dt_senha=row["dt_senha"],
                operador_execucao=row["operador_execucao"],
                operador_senha=row["operador_senha"]
                if not pd.isna(row["operador_senha"])
                else None,
                operador_canc=row["operador_canc"]
                if not pd.isna(row["operador_canc"])
                else None,
                observacao=row["observacao"]
                if not pd.isna(row["observacao"])
                else None,
                dt_base=row["dt_base"],
                file_name=row["file_name"],
            )
        except Exception as e:
            logger.error(
                f"Error creating AtendimentoSaoLucasBronzeSchema object: {e}"
            )
            raise e
        else:
            return service_data

    def get_service_by_guia_procedimento(
        self, session: Session, guia: str, procedimento: str
    ) -> AtendimentosBronzeModel | None:
        """
        Retrieve an AtendimentosSaoLucasBronze record from the database based on guia and procedimento.

        Args:
            session (Session): The database session to use for the query.
            guia (str): The guia value to filter by.
            procedimento (str): The procedimento value to filter by.

        Returns:
            AtendimentosBronzeModel | None: The retrieved record if found, otherwise None.
        """
        try:
            stmt = select(AtendimentosBronzeModel).where(
                AtendimentosBronzeModel.guia == guia,
                AtendimentosBronzeModel.procedimento == procedimento,
            )
            result = session.execute(stmt).scalar_one_or_none()
        except Exception as e:
            logger.error(
                f"Error retrieving service by guia and procedimento: {e} - Guia: {guia}, Procedimento: {procedimento}"
            )
            raise
        else:
            if result:
                logger.info(
                    f"Service retrieved successfully for guia: {guia} and procedimento: {procedimento}"
                )
            else:
                logger.info(
                    f"No service found for guia: {guia} and procedimento: {procedimento}"
                )
            return result

    def insert_or_update_services(
        self, session: Session, service_data: AtendimentoSaoLucasBronzeSchema
    ) -> None:
        """
        Insert or update AtendimentosSaoLucasBronze records in the session (without committing).

        Args:
            session (Session): The database session to use for the operation.
            service_data (AtendimentoSaoLucasBronzeSchema): The data to insert or update.
        """
        try:
            existing_service = self.get_service_by_guia_procedimento(
                session, service_data.guia, service_data.procedimento
            )
            if existing_service:
                for field, value in service_data.model_dump().items():
                    setattr(existing_service, field, value)
                session.add(existing_service)
                logger.info(
                    f"Service updated successfully for guia: {service_data.guia} and procedimento: {service_data.procedimento}"
                )
            else:
                new_service = AtendimentosBronzeModel(**service_data.model_dump())
                session.add(new_service)
                logger.info(
                    f"Service inserted successfully for guia: {service_data.guia} and procedimento: {service_data.procedimento}"
                )
        except Exception as e:
            logger.error(f"Error inserting or updating services: {e}")
            raise

    def move_file(self) -> None:
        """
        Move the processed file from the landzone directory to the processed directory.
        """
        try:
            files = os.listdir(self.landzone_path)
            for file in files:
                if os.path.splitext(file.lower())[0] == self.file_name:
                    source_file = os.path.join(self.landzone_path, file)
                    destination_file = os.path.join(self.processed_path, file)
                    os.rename(source_file, destination_file)
                    logger.info(
                        f"File moved successfully from {source_file} to {destination_file}"
                    )
        except Exception as e:
            logger.error(
                f"Error moving file from {source_file} to {destination_file}: {e}"
            )
            raise

    def main(self) -> bool:
        """
        Main method to run the atendimento sao lucas import pipeline.
        """
        logger.info("ATENDIMENTOS SAO LUCAS IMPORT")
        try:
            df = self.load_data()
            df = self.add_control_columns(df)

            num_rows = len(df)
            affected_rows = 0

            with db.session_factory() as session:
                try:
                    for _, row in df.iterrows():
                        service_data = self.create_service_data(row)
                        self.insert_or_update_services(session, service_data)
                        affected_rows += 1
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

            logger.info(f"Total rows processed: {num_rows}")
            logger.info(f"Total affected rows: {affected_rows}")

            self.move_file()
        except Exception as e:
            logger.error(f"Error in Atendimentos Sao Lucas import pipeline: {e}")
            return False
        else:
            logger.info("IMPORT ATENDIMENTOS SAO LUCAS COMPLETED SUCCESSFULLY!")
            return True
