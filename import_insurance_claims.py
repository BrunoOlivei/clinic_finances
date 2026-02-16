import pandas as pd

from core import db, logger
from schemas import InsuranceClaimCreate
from services import InsuranceClaimService
from services.read_csv import ReadCSV


class IngestInsuranceClaims:
    def __init__(self):
        self.csv_reader = ReadCSV()

    def sanitize_claim_columns(self, claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and sanitizes the DataFrame columns.

        Args:
            claims_df (pd.DataFrame): The original DataFrame.

        Returns:
            pd.DataFrame: The sanitized DataFrame.
        """
        try:
            new_columns = [
                "nr_claim",
                "nr_request",
                "cd_patient",
                "dt_issue",
                "Atendimento",
                "Horário",
                "dm_service",
                "st_claim",
                "tp_claim",
                "fg_return",
                "cd_procedure",
                "nm_procedure",
                "qt_procedure",
            ]

            claims_df.columns = new_columns
            return claims_df
        except Exception as e:
            logger.error(f"Error sanitizing claim columns: {e}")
            raise

    def format_date_columns(self, claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the date columns in the DataFrame.

        Args:
            claims_df (pd.DataFrame): The DataFrame with claim data.

        Returns:
            pd.DataFrame: The DataFrame with formatted date columns.
        """
        try:
            claims_df["dt_issue"] = claims_df[["dt_issue"]].apply(
                lambda x: pd.to_datetime(
                    x, format="%d/%m/%Y", errors="coerce", dayfirst=True
                )
            )

            claims_df["dm_service"] = claims_df[["Atendimento", "Horário"]].apply(
                lambda x: pd.to_datetime(
                    f"{x['Atendimento']} {x['Horário']}",
                    format="%d/%m/%Y %H:%M:%S",
                    errors="coerce",
                    dayfirst=True,
                ),
                axis=1,
            )
            claims_df.drop(columns=["Atendimento", "Horário"], inplace=True)
            return claims_df
        except Exception as e:
            logger.error(f"Error formatting date columns: {e}")
            raise

    def sanitize_claim_data(self, claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and sanitizes the claim data in the DataFrame.

        Args:
            claims_df (pd.DataFrame): The DataFrame with claim data.

        Returns:
            pd.DataFrame: The sanitized DataFrame.
        """
        try:
            claims_df["nr_request"] = claims_df[["nr_request"]].apply(
                lambda x: (
                    x.str.replace(r"\s+", " ", regex=True)
                    .str.strip()
                    .replace(r"Solicitacao: C", "", regex=True)
                )
            )
            claims_df["st_claim"] = claims_df[["st_claim"]].apply(
                lambda x: x.str.replace(r"\s+", " ", regex=True).str.strip()
            )
            claims_df["tp_claim"] = claims_df[["tp_claim"]].apply(
                lambda x: x.str.replace(r"\s+", " ", regex=True).str.strip()
            )
            claims_df["fg_return"] = claims_df[["fg_return"]].apply(
                lambda x: (
                    x.str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
                    == "sim"
                )
            )
            claims_df["nm_procedure"] = claims_df[["nm_procedure"]].apply(
                lambda x: x.str.replace(r"\s+", " ", regex=True).str.strip()
            )
            return claims_df
        except Exception as e:
            logger.error(f"Error sanitizing claim data: {e}")
            raise

    def create_claim_data(self, row: pd.Series) -> InsuranceClaimCreate:
        """
        Creates an InsuranceClaimCreate object from a DataFrame row.

        Args:
            row (pd.Series): A row from the DataFrame.

        Returns:
            InsuranceClaimCreate: The created InsuranceClaimCreate object.
        """
        try:
            return InsuranceClaimCreate(
                nr_claim=row["nr_claim"],
                nr_request=row["nr_request"],
                cd_patient=row["cd_patient"],
                dt_issue=row["dt_issue"],
                dm_service=row["dm_service"],
                st_claim=row["st_claim"],
                tp_claim=row["tp_claim"],
                fg_return=row["fg_return"],
                cd_procedure=row["cd_procedure"],
                nm_procedure=row["nm_procedure"],
                qt_procedure=row["qt_procedure"],
            )
        except Exception as e:
            logger.error(f"Error creating claim data: {e}")
            raise

    def import_from_csv(
        self, year: int | None = None, month: int | None = None
    ) -> list[InsuranceClaimCreate]:
        """
        Imports insurance claims from a CSV file.

        Args:
            year (int | None, optional): The year for the CSV file. Defaults to None.
            month (int | None, optional): The month for the CSV file. Defaults to None.

        Returns:
            list[InsuranceClaimCreate]: A list of InsuranceClaimCreate objects created from the CSV data.
        """
        try:
            df = self.csv_reader.read(year, month)

            df["dm_service"] = pd.to_datetime(None)
            claims_df = df[
                [
                    "Guia",
                    "Observação",
                    "Cd Beneficiário",
                    "Emissão",
                    "Atendimento",
                    "Horário",
                    "dm_service",
                    "Status",
                    "Tipo",
                    "Retorno",
                    "Procedimento",
                    "Procedimento.1",
                    "Quantidade",
                ]
            ].copy()

            claims_df = self.sanitize_claim_columns(claims_df)
            claims_df = self.format_date_columns(claims_df)
            claims_df = self.sanitize_claim_data(claims_df)

            claims_data = []
            for _, row in claims_df.iterrows():
                claims_data.append(self.create_claim_data(row))

            logger.info(f"Successfully imported {len(claims_data)} insurance claims")
            return claims_data
        except Exception as e:
            logger.error(f"Error importing insurance claims: {e}")
            raise

    def insert_or_update_claims(
        self, service: InsuranceClaimService, claims_data: list[InsuranceClaimCreate]
    ) -> None:
        """
        Inserts or updates insurance claims in the database.

        Args:
            service (InsuranceClaimService): The service to handle insurance claim operations.
            claims_data (list[InsuranceClaimCreate]): A list of InsuranceClaimCreate objects to be inserted or updated.
        """
        inserted_num = 0
        updated_num = 0
        try:
            for claim_data in claims_data:
                existing_claim = service.get_by_claim_number(claim_data.nr_claim)
                if existing_claim:
                    logger.info(f"Updating existing claim: {claim_data.nr_claim}")
                    service.update(claim_data.nr_claim, claim_data)
                    updated_num += 1
                else:
                    logger.info(f"Inserting new claim: {claim_data.nr_claim}")
                    service.create(claim_data)
                    inserted_num += 1
            logger.info(f"Inserted {inserted_num} new claims.")
            logger.info(f"Updated {updated_num} existing claims.")
        except Exception as e:
            logger.error(f"Error inserting/updating insurance claims: {e}")
            raise

    def run(self, year: int | None = None, month: int | None = None) -> None:
        """
        Runs the insurance claim import process.

        Args:
            year (int | None, optional): The year for the CSV file. Defaults to None.
            month (int | None, optional): The month for the CSV file. Defaults to None.
        """
        logger.info("INSURANCE CLAIM IMPORT")

        claims_data = self.import_from_csv(year, month)

        with db.session_factory() as session:
            claim_service = InsuranceClaimService(session=session)
            self.insert_or_update_claims(claim_service, claims_data)

            total_claims = claim_service.count()
            logger.info(f"Total insurance claims in database: {total_claims}")

        logger.success("IMPORT COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    IngestInsuranceClaims().run(
        year=2026,
        month=1
    )
