import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core import db, logger, set_default_dt_base
from src.models import AtendimentosSaoLucasBronze as AtendimentosBronzeModel
from src.models import AtendimentosSaoLucasSilver as AtendimentosSilverModel
from src.schemas import AtendimentoSaoLucasSilverSchema


class AtendimentosSaoLucasSilver:
    def __init__(
        self,
        dt_base: int | None = None,
    ) -> None:
        self.dt_base = set_default_dt_base(dt_base)
        self.file_name = f"{self.dt_base}_atendimentos_sao_lucas"
        self.schema = {
            "terminal": {
                "type": str,
            },
            "guia": {
                "type": int,
            },
            "emissao": {
                "type": "date",
                "format": "%d/%m/%Y",
            },
            "atendimento": {
                "type": "date",
                "format": "%d/%m/%Y",
            },
            "horario": {
                "type": "time",
                "format": "%H:%M:%S",
            },
            "emissao_tiss": {
                "type": "date",
                "format": "%d/%m/%Y",
            },
            "cd_beneficiario": {
                "type": str,
            },
            "beneficiario": {
                "type": str,
            },
            "endereco_beneficiario": {
                "type": str,
            },
            "solicitante": {
                "type": str,
            },
            "solicitante_1": {
                "type": str,
            },
            "especialidade": {
                "type": str,
            },
            "status": {
                "type": str,
            },
            "tipo": {
                "type": str,
            },
            "retorno": {
                "type": bool,
            },
            "senha_terapia": {
                "type": str,
            },
            "procedimento": {
                "type": str,
            },
            "procedimento_1": {
                "type": str,
            },
            "quantidade": {
                "type": int,
            },
            "sessoes_executadas": {
                "type": "nullable_int",
            },
            "prestador": {
                "type": str,
            },
            "prestador_1": {
                "type": str,
            },
            "especialidade_1": {
                "type": str,
            },
            "indicacao_clinica": {
                "type": str,
            },
            "status_export": {
                "type": str,
            },
            "dt_export": {
                "type": "date",
                "format": "%d/%m/%Y",
            },
            "dt_senha": {
                "type": "date",
                "format": "%d/%m/%Y",
            },
            "operador_execucao": {
                "type": str,
            },
            "operador_senha": {
                "type": str,
            },
            "operador_canc": {
                "type": str,
            },
            "observacao": {
                "type": str,
            },
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
            stmt = select(AtendimentosBronzeModel).where(
                AtendimentosBronzeModel.file_name == self.file_name,
                AtendimentosBronzeModel.silver_exported == False,  # noqa: E712
            )
            df = pd.read_sql_query(stmt, session.connection())
        except Exception as e:
            logger.error(f"Error loading data for Atendimentos Sao Lucas Silver: {e}")
            raise
        else:
            logger.info(
                f"Data loaded successfully for Atendimentos Sao Lucas Silver: {self.file_name}"
            )
            return df

    def format_type_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format the data types of the DataFrame columns according to the defined schema.

        Args:
            df (pd.DataFrame): The DataFrame to be formatted.

        Returns:
            pd.DataFrame: The DataFrame with formatted data types.
        """
        for column, properties in self.schema.items():
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
            elif properties["type"] == "nullable_int":
                df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
            else:
                df[column] = df[column].astype(properties["type"])
        return df

    def create_service_data(self, row: pd.Series) -> AtendimentoSaoLucasSilverSchema:
        """
        Create an AtendimentoSaoLucasSilverSchema object from a row of the DataFrame.

        Args:
            row (pd.Series): A row from the DataFrame.

        Returns:
            AtendimentoSaoLucasSilverSchema: The created schema object.
        """
        try:
            service_data = AtendimentoSaoLucasSilverSchema(
                cd_terminal=row["terminal"],
                nr_guia=row["guia"],
                dt_emissao=row["emissao"],
                dt_atendimento=row["atendimento"],
                hr_atendimento=row["horario"],
                dt_emissao_tiss=row["emissao_tiss"],
                cd_beneficiario=row["cd_beneficiario"],
                nm_beneficiario=row["beneficiario"]
                if not pd.isna(row["beneficiario"])
                else None,
                ds_endereco_beneficiario=row["endereco_beneficiario"]
                if not pd.isna(row["endereco_beneficiario"])
                else None,
                cd_solicitante=row["solicitante"],
                nm_solicitante=row["solicitante_1"],
                ds_especialidade=row["especialidade"],
                st_atendimento=row["status"],
                tp_atendimento=row["tipo"],
                fg_retorno=row["retorno"],
                cd_senha_terapia=row["senha_terapia"]
                if not pd.isna(row["senha_terapia"])
                else None,
                cd_procedimento=row["procedimento"],
                ds_procedimento=row["procedimento_1"],
                qt_procedimento=row["quantidade"],
                qt_sessoes_executadas=row["sessoes_executadas"],
                cd_prestador=row["prestador"],
                nm_prestador=row["prestador_1"],
                ds_especialidade_prestador=row["especialidade_1"],
                ds_indicacao_clinica=row["indicacao_clinica"]
                if not pd.isna(row["indicacao_clinica"])
                else None,
                st_export=row["status_export"],
                dt_export=row["dt_export"],
                dt_senha=row["dt_senha"],
                cd_operador_execucao=row["operador_execucao"],
                cd_operador_senha=row["operador_senha"]
                if not pd.isna(row["operador_senha"])
                else None,
                cd_operador_cancelamento=row["operador_canc"]
                if not pd.isna(row["operador_canc"])
                else None,
                ds_observacao=row["observacao"]
                if not pd.isna(row["observacao"])
                else None,
                dt_base=row["dt_base"],
                file_name=row["file_name"],
            )
        except Exception as e:
            logger.error(
                f"Error creating AtendimentoSaoLucasSilverSchema object: {e} - Row data: {row.to_dict()}"
            )
            raise
        else:
            logger.info(
                f"AtendimentoSaoLucasSilverSchema object created successfully for atendimento {service_data.dt_atendimento}"
            )
            return service_data

    def get_service_by_guia_procedimento(
        self, session: Session, nr_guia: int, cd_procedimento: str
    ) -> AtendimentosSilverModel | None:
        """
        Retrieve an AtendimentosSaoLucasSilver record from the database based on nr_guia and cd_procedimento.

        Args:
            session (Session): The database session to use for the query.
            nr_guia (int): The guia value to filter by.
            cd_procedimento (str): The procedimento value to filter by.

        Returns:
            AtendimentosSilverModel | None: The retrieved record if found, otherwise None.
        """
        try:
            stmt = select(AtendimentosSilverModel).where(
                AtendimentosSilverModel.nr_guia == nr_guia,
                AtendimentosSilverModel.cd_procedimento == cd_procedimento,
            )
            result = session.execute(stmt).scalar_one_or_none()
        except Exception as e:
            logger.error(
                f"Error retrieving service by nr_guia and cd_procedimento: {e} - nr_guia: {nr_guia}, cd_procedimento: {cd_procedimento}"
            )
            raise
        else:
            if result:
                logger.info(
                    f"Service retrieved successfully for nr_guia: {nr_guia} and cd_procedimento: {cd_procedimento}"
                )
            else:
                logger.info(
                    f"No service found for nr_guia: {nr_guia} and cd_procedimento: {cd_procedimento}"
                )
            return result

    def insert_or_update_services(
        self, session: Session, service_data: AtendimentoSaoLucasSilverSchema
    ) -> None:
        """
        Insert or update AtendimentosSaoLucasSilver records in the session (without committing).

        Args:
            session (Session): The database session to use for the operation.
            service_data (AtendimentoSaoLucasSilverSchema): The data to insert or update.
        """
        try:
            existing_service = self.get_service_by_guia_procedimento(
                session, service_data.nr_guia, service_data.cd_procedimento
            )
            if existing_service:
                for field, value in service_data.model_dump().items():
                    setattr(existing_service, field, value)
                session.add(existing_service)
                logger.info(
                    f"Service updated successfully for nr_guia: {service_data.nr_guia} and cd_procedimento: {service_data.cd_procedimento}"
                )
            else:
                new_service = AtendimentosSilverModel(**service_data.model_dump())
                session.add(new_service)
                logger.info(
                    f"Service inserted successfully for nr_guia: {service_data.nr_guia} and cd_procedimento: {service_data.cd_procedimento}"
                )
        except Exception as e:
            logger.error(f"Error inserting or updating services: {e}")
            raise

    def main(self) -> bool:
        """
        Main method to run the atendimento sao lucas silver import pipeline.
        """
        logger.info("ATENDIMENTOS SAO LUCAS SILVER IMPORT")
        try:
            with next(db.get_session()) as session:
                df = self.load_data(session)
                df = self.format_type_data(df)

                num_rows = len(df)
                affected_rows = 0

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
        except Exception as e:
            logger.error(f"Error in Atendimentos Sao Lucas Silver pipeline: {e}")
            return False
        else:
            logger.info("IMPORT ATENDIMENTOS SAO LUCAS SILVER COMPLETED SUCCESSFULLY!")
            return True
