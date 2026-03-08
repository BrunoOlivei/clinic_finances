import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core import db, format_type_data, logger, set_default_dt_base
from src.models import SolicitacoesSaoLucasBronze as SolicitacoesBronzeModel
from src.models import SolicitacoesSaoLucasSilver as SolicitacoesSilverModel
from src.schemas import SolicitacoesSaoLucasSilverSchema


class SolicitacoesSaoLucasSilver:
    """
    Service class for processing and transforming data from the "tb_solicitacoes_sao_lucas" table in the bronze layer
    and loading it into the silver layer. This class includes methods for data extraction, transformation,
    and loading (ETL) of claims data imported from the São Lucas operator, as well as validation and error handling.

    Args:
        ReadFile (_type_): Utility class for reading files from various sources (e.g., local filesystem, cloud storage).
        db (_type_): Database session manager for handling database connections and transactions.
        logger (_type_): Logger instance for logging messages and errors during the ingestion process.
    """

    def __init__(
        self,
        dt_base: int | None = None,
    ) -> None:
        self.dt_base = set_default_dt_base(dt_base)
        self.file_name = f"{self.dt_base}_solicitacoes_sao_lucas"
        self.schema = {
            "solicitacao": {"type": "integer"},
            "data": {"type": "datetime", "format": "%d/%m/%Y %H:%M:%S"},
            "validade_solicitacao": {"type": "date", "format": "%d/%m/%Y"},
            "solicitante": {"type": "string"},
            "operador": {"type": "string"},
            "terminal": {"type": "string"},
            "solicitante_1": {"type": "string"},
            "beneficiario": {"type": "string"},
            "beneficiario_1": {"type": "string"},
            "especialidade": {"type": "string"},
            "procedimento": {"type": "string"},
            "procedimento_1": {"type": "string"},
            "qtde_sol": {"type": "integer"},
            "qtde_lib": {"type": "integer"},
            "qtde_exe": {"type": "integer"},
            "prestador": {"type": "string"},
            "especialidade_prestador": {"type": "string"},
            "status": {"type": "string"},
            "especificacao": {"type": "string"},
            "tipo_de_solicitacao": {"type": "string"},
            "operador_cancelamento": {"type": "string"},
            "observacao": {"type": "string"},
            "auditor": {"type": "string"},
            "data_agendamento": {"type": "date", "format": "%d/%m/%Y"},
            "operador_agendamento": {"type": "string"},
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
            stmt = select(SolicitacoesBronzeModel).where(
                SolicitacoesBronzeModel.file_name == self.file_name,
                SolicitacoesBronzeModel.silver_exported == False,  # noqa: E712
            )
            df = pd.read_sql_query(stmt, session.connection())
        except Exception as e:
            logger.error(f"Error loading data for Solicitações Sao Lucas Bronze: {e}")
            raise
        else:
            logger.info(
                f"Data loaded succesfully for Solicitações Sao Lucas Bronze: {self.file_name}"
            )
            return df

    def creat_claim_data(self, row: pd.Series) -> SolicitacoesSaoLucasSilverSchema:
        """
        Create an SolicitacoesSaoLucasSilverSchema object from a row of the DataFrame.

        Args:
            row (pd.Series): A row from the DataFrame.

        Returns:
            SolicitacoesSaoLucasSilverSchema: The created schema object.
        """
        try:
            claim_data = SolicitacoesSaoLucasSilverSchema(
                nr_solicitacao=row["solicitacao"],
                dt_solicitacao=row["data"],
                dt_validade_solicitacao=row["validade_solicitacao"],
                cd_solicitante=row["solicitante"],
                cd_operador=row["operador"],
                nm_terminal=row["terminal"] if not pd.isna(row["terminal"]) else None,
                nm_solicitante=row["solicitante_1"],
                cd_beneficiario=row["beneficiario"],
                nm_beneficiario=row["beneficiario_1"]
                if not pd.isna(row["beneficiario_1"])
                else None,
                ds_especialidade=row["especialidade"],
                cd_procedimento=row["procedimento"],
                nm_procedimento=row["procedimento_1"],
                qt_solicitado=row["qtde_sol"],
                qt_liberado=row["qtde_lib"],
                qt_executado=row["qtde_exe"],
                cd_prestador=row["prestador"]
                if not pd.isna(row["prestador"])
                else None,
                ds_especialidade_prestador=row["especialidade_prestador"]
                if not pd.isna(row["especialidade_prestador"])
                else None,
                st_solicitacao=row["status"],
                ds_especificacao=row["especificacao"]
                if not pd.isna(row["especificacao"])
                else None,
                tp_solicitacao=row["tipo_de_solicitacao"],
                cd_operador_cancelamento=row["operador_cancelamento"]
                if not pd.isna(row["operador_cancelamento"])
                else None,
                ds_observacao=row["observacao"]
                if not pd.isna(row["observacao"])
                else None,
                cd_auditor=row["auditor"] if not pd.isna(row["auditor"]) else None,
                dt_agendamento=row["data_agendamento"]
                if not pd.isna(row["data_agendamento"])
                else None,
                cd_operador_agendamento=row["operador_agendamento"]
                if not pd.isna(row["operador_agendamento"])
                else None,
                dt_base=row["dt_base"],
                file_name=row["file_name"],
            )
        except Exception as e:
            logger.error(
                f"Error creating SolicitacoesSaoLucasSilverSchema object: {e} - Row data: {row.to_dict()}"
            )
            raise
        else:
            logger.info(
                f"SolicitacoesSaoLucasSilverSchema object created successfully for atendimento {claim_data.dt_solicitacao}"
            )
            return claim_data

    def get_claim_by_solicitacao_procedimento(
        self, session: Session, nr_solicitacao: int, cd_procedimento: str
    ) -> SolicitacoesSilverModel | None:
        """
        Retrieve an SolicitacoesSilverModel record from the database based on nr_solicitacao and cd_procedimento.

        Args:
            session (Session): The database session to use for the query.
            nr_solicitacao (int): The solicitacao value to filter by.
            cd_procedimento (str): The procedimento value to filter by.

        Returns:
            SolicitacoesSilverModel | None: The retrieved record if found, otherwise None.
        """
        try:
            stmt = select(SolicitacoesSilverModel).where(
                SolicitacoesSilverModel.nr_solicitacao == nr_solicitacao,
                SolicitacoesSilverModel.cd_procedimento == cd_procedimento,
            )
            result = session.execute(stmt).scalar_one_or_none()
        except Exception as e:
            logger.error(
                f"Error retrieving service by nr_solicitacao and cd_procedimento: {e} - nr_solicitacao: {nr_solicitacao}, cd_procedimento: {cd_procedimento}"
            )
            raise
        else:
            if result:
                logger.info(
                    f"Claim retrieved successfully for nr_solicitacao: {nr_solicitacao} and cd_procedimento: {cd_procedimento}"
                )
            else:
                logger.info(
                    f"No claim found for nr_solicitacao: {nr_solicitacao} and cd_procedimento {cd_procedimento}"
                )
            return result

    def insert_or_update_claims(
        self, session: Session, claim_data: SolicitacoesSaoLucasSilverSchema
    ) -> None:
        """
        Insert or update SolicitacoesSaoLucasSilver records in the session (without committing).

        Args:
            session (Session): The database session to use for the operation.
            claim_data (SolicitacoesSaoLucasSilverSchema): The data to insert or update.
        """
        try:
            existing_claim = self.get_claim_by_solicitacao_procedimento(
                session, claim_data.nr_solicitacao, claim_data.cd_procedimento
            )
            if existing_claim:
                for field, value in claim_data.model_dump().items():
                    setattr(existing_claim, field, value)
                session.add(existing_claim)
                logger.info(
                    f"Claim updated successfully for nr_solicitacao: {claim_data.nr_solicitacao} and cd_procedimento: {claim_data.cd_procedimento}"
                )
            else:
                new_claim = SolicitacoesSilverModel(**claim_data.model_dump())
                session.add(new_claim)
                logger.info(
                    f"Claim inserted successfully for nr_solicitacao: {claim_data.nr_solicitacao} and cd_procedimento: {claim_data.cd_procedimento}"
                )
        except Exception as e:
            logger.error(f"Error inserting or updating claims: {e}")
            raise

    def main(self) -> bool:
        """
        Main methos to run the recibos sao lucas silver import pipeline
        """
        logger.info("SOLICITACOES SAO LUCAS SILVER IMPORT")
        try:
            with next(db.get_session()) as session:
                df = self.load_data(session)
                df = format_type_data(df, self.schema)

                num_rows = len(df)
                affected_rows = 0

                try:
                    for _, row in df.iterrows():
                        claim_data = self.creat_claim_data(row)
                        self.insert_or_update_claims(session, claim_data)
                        affected_rows += 1
                    session.commit()
                except Exception:
                    session.rollback()
                    raise

            logger.info(f"Total rows processed: {num_rows}")
            logger.info(f"Total affected rows: {affected_rows}")
        except Exception as e:
            logger.error(f"Error in Solicitacoes Sao Lucas Silver pipeline: {e}")
            return False
        else:
            logger.info("IMPORT SOLICITACOES SAO LUCAS SILVER COMPLETED SUCCESSFULLY!")
            return True
