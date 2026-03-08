import os

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core import ReadFile, db, logger, set_default_dt_base
from src.models import SolicitacoesSaoLucasBronze as SolicitacoesBronzeModel
from src.schemas import SolicitacoesSaoLucasBronzeSchema


class SolicitacoesSaoLucasBronze:
    """
    Service class for handling the ingestion of "Solicitações" data from the São Lucas operator into the bronze layer.
    This class includes methods for reading the source file, validating and transforming the data, and inserting it into the database.

    Args:
        ReadFile (_type_): Utility class for reading files from various sources (e.g., local filesystem, cloud storage).
        db (_type_): Database session manager for handling database connections and transactions.
        logger (_type_): Logger instance for logging messages and errors during the ingestion process.
        set_default_dt_base (_type_): Utility function for setting a default base date (dt_base) if not provided in the data.
    """

    def __init__(
        self,
        dt_base: int | None = None,
    ) -> None:
        self.solicitacoes_sao_lucas_data_path = "./data/solicitacoes_sao_lucas"
        self.dt_base = set_default_dt_base(dt_base)
        self.landzone_path = f"{self.solicitacoes_sao_lucas_data_path}/landzone/"
        self.processed_path = f"{self.solicitacoes_sao_lucas_data_path}/processed/"
        self.file_name = f"{self.dt_base}_solicitacoes_sao_lucas"

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
            logger.error(f"Error loading data for Solicitacoes Sao Lucas Bronze: {e}")
            raise
        else:
            logger.info(
                f"Data loaded successfully for Solicitacoes Sao Lucas Bronze: {self.file_name}"
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
                f"Error adding control columns for Solicitacoes Sao Lucas Bronze: {e}"
            )
            raise
        else:
            logger.info(
                f"Columns dt_base and file_name added successfully for Solicitacoes Sao Lucas Bronze: {self.file_name}"
            )
            return df

    def create_claims_data(self, row: pd.Series) -> SolicitacoesSaoLucasBronzeSchema:
        """
        Create a SolicitacoesSaoLucasBronzeSchema object from a row of the DataFrame.

        Args:
            row (pd.Series): A row from the DataFrame.
        
        Returns:
            SolicitacoesSaoLucasBronzeSchema: The created schema object
        """
        try:
            claim_data = SolicitacoesSaoLucasBronzeSchema(
                solicitacao=row["solicitacao"],
                data=row["data"],
                validade_solicitacao=row["validade_solicitacao"],
                solicitante=row["solicitante"],
                operador=row["operador"],
                terminal=row["terminal"] if not pd.isna(row["terminal"]) else None,
                solicitante_1=row["solicitante_1"],
                beneficiario=row["beneficiario"],
                beneficiario_1=row["beneficiario_1"],
                especialidade=row["especialidade"],
                procedimento=row["procedimento"],
                procedimento_1=row["procedimento_1"],
                qtde_sol=row["qtde_sol"],
                qtde_lib=row["qtde_lib"],
                qtde_exe=row["qtde_exe"],
                prestador=row["prestador"] if not pd.isna(row["prestador"]) else None,
                especialidade_prestador=row["especialidade_prestador"] if not pd.isna(row["especialidade_prestador"]) else None,
                status=row["status"],
                especificacao=row["especificacao"] if not pd.isna(row["especificacao"]) else None,
                tipo_de_solicitacao=row["tipo_de_solicitacao"],
                operador_cancelamento=row["operador_cancelamento"] if not pd.isna(row["operador_cancelamento"]) else None,
                observacao=row["observacao"] if not pd.isna(row["observacao"]) else None,
                auditor=row["auditor"] if not pd.isna(row["auditor"]) else None,
                data_agendamento=row["data_agendamento"] if not pd.isna(row["data_agendamento"]) else None,
                operador_agendamento=row["operador_agendamento"] if not pd.isna(row["operador_agendamento"]) else None,
                dt_base=row["dt_base"],
                file_name=row["file_name"],
            )
        except Exception as e:
            logger.error(
                f"Error creating claim data for Solicitacoes Sao Lucas Bronze: {e}"
            )
            raise
        else:
            return claim_data

    def get_claim_by_solicitacao_procedimento(self, session: Session, solicitacao: str, procedimento: str) -> SolicitacoesBronzeModel | None:
        """
        Retrieve a claim from the database based on the solicitacao and procedimento.

        Args:
            session (Session): The database session to use for the query.
            solicitacao (str): The solicitacao number to search for.
            procedimento (str): The procedure code to search for.

        Returns:
            SolicitacoesBronzeModel | None: The retrieved claim object if found, otherwise None.
        """
        try:
            stmt = select(SolicitacoesBronzeModel).where(
                SolicitacoesBronzeModel.solicitacao == solicitacao,
                SolicitacoesBronzeModel.procedimento == procedimento,
            )
            result = session.execute(stmt).scalar_one_or_none()
            return result
        except Exception as e:
            logger.error(
                f"Error retrieving claim by solicitacao {solicitacao} and procedimento {procedimento}: {e}"
            )
            raise
        else:
            if result:
                logger.info(
                    f"Claim retrieved successfully for solicitacao {solicitacao} and procedimento {procedimento}"
                )
            else:
                logger.info(
                    f"No claim found for solicitacao {solicitacao} and procedimento {procedimento}"
                )
            return result

    def insert_or_update_claims(
        self, session: Session, claim_data: SolicitacoesSaoLucasBronzeSchema
    ) -> None:
        """
        Insert a new claim into the database or update an existing claim if it already exists.

        Args:
            session (Session): The database session to use for the operation.
            claim_data (SolicitacoesSaoLucasBronzeSchema): The claim data to be inserted or updated.
        """
        try:
            existing_claim = self.get_claim_by_solicitacao_procedimento(
                session, claim_data.solicitacao, claim_data.procedimento
            )
            if existing_claim:
                for field, value in claim_data.dict().items():
                    setattr(existing_claim, field, value)
                session.add(existing_claim)
                logger.info(
                    f"Claim updated successfully for solicitacao {claim_data.solicitacao} and procedimento {claim_data.procedimento}"
                )
            else:
                new_claim = SolicitacoesBronzeModel(**claim_data.dict())
                session.add(new_claim)
                logger.info(
                    f"Claim inserted successfully for solicitacao {claim_data.solicitacao} and procedimento {claim_data.procedimento}"
                )
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(
                f"Error inserting or updating claim for solicitacao {claim_data.solicitacao} and procedimento {claim_data.procedimento}: {e}"
            )
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
        logger.info("SOLICITACOES SAO LUCAS IMPORT")
        try:
            df = self.load_data()
            df = self.add_control_columns(df)

            num_rows = len(df)
            affected_rows = 0

            with next(db.get_session()) as session:
                try:
                    for _, row in df.iterrows():
                        claim_data = self.create_claims_data(row)
                        self.insert_or_update_claims(session, claim_data)
                        affected_rows += 1
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

            logger.info(f"Total rows processed: {num_rows}")
            logger.info(f"Total affected rows: {affected_rows}")

            self.move_file()
        except Exception as e:
            logger.error(f"Error in Solicitações Sao Lucas import pipeline: {e}")
            return False
        else:
            logger.info("IMPORT SOLICITACOES SAO LUCAS COMPLETED SUCCESSFULLY!")
            return True


            