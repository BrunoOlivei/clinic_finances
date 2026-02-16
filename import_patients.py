import pandas as pd

from core import db, logger
from schemas import PatientCreate
from services import PatientService
from services.read_csv import ReadCSV


class IngestPatients:
    def __init__(self):
        self.csv_reader = ReadCSV()

    def sanitize_patient_columns(self, patients_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and sanitizes the DataFrame columns.

        Args:
            patients_df (pd.DataFrame): The original DataFrame.

        Returns:
            pd.DataFrame: The sanitized DataFrame.
        """
        try:
            patients_df.columns = ["cd_patient", "nm_patient", "ds_address"]
            return patients_df
        except Exception as e:
            logger.error(f"Error sanitizing patient columns: {e}")
            raise

    def sanitize_patient_data(self, patients_df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans and sanitizes the patient data in the DataFrame.

        Args:
            patients_df (pd.DataFrame): The DataFrame with patient data.

        Returns:
            pd.DataFrame: The sanitized DataFrame.
        """
        try:
            for col in ["nm_patient", "ds_address", "cd_patient"]:
                patients_df[[col]] = patients_df[[col]].apply(
                    lambda x: x.str.replace(r"\s+", " ", regex=True).str.strip()
                )
            return patients_df
        except Exception as e:
            logger.error(f"Error sanitizing patient data: {e}")
            raise

    def remove_patient_duplicates(self, patients_df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes duplicate patients based on the 'cd_patient' column.

        Args:
            patients_df (pd.DataFrame): The DataFrame with patient data.

        Returns:
            pd.DataFrame: The DataFrame with duplicates removed.
        """
        try:
            return patients_df.drop_duplicates(subset="cd_patient", keep="first")
        except Exception as e:
            logger.error(f"Error removing duplicate patients: {e}")
            raise

    def create_patient_data(self, row: pd.Series) -> PatientCreate:
        """
        Creates a PatientCreate object from a DataFrame row.

        Args:
            row (pd.Series): A row from the DataFrame.

        Returns:
            PatientCreate: The created PatientCreate object.
        """
        try:
            return PatientCreate(
                cd_patient=row["cd_patient"],
                nm_patient=row["nm_patient"],
                ds_address=row["ds_address"],
            )
        except Exception as e:
            logger.error(f"Error creating patient data: {e}")
            raise

    def import_from_csv(
        self, year: int | None = None, month: int | None = None
    ) -> list[PatientCreate]:
        """
        Imports patient data from a CSV file and returns a list of PatientCreate objects.

        Args:
            year (int | None, optional): The year for the CSV file. Defaults to None
            month (int | None, optional): The month for the CSV file. Defaults to None.

        Returns:
            list[PatientCreate]: A list of PatientCreate objects created from the CSV data.
        """
        try:
            df = self.csv_reader.read(year, month)

            patients_df = df[
                ["Cd Beneficiário", "Beneficiário", "Endereço Beneficiário"]
            ].copy()

            patients_df = self.sanitize_patient_columns(patients_df)
            patients_df = self.sanitize_patient_data(patients_df)
            patients_df = self.remove_patient_duplicates(patients_df)

            patients_data = []
            for _, row in patients_df.iterrows():
                patients_data.append(self.create_patient_data(row))

            return patients_data
        except Exception as e:
            logger.error(f"Error importing patients from CSV: {e}")
            raise

    def insert_or_update_patients(
        self, service: PatientService, patients_data: list[PatientCreate]
    ) -> None:
        """
        Inserts or updates patients in the database.

        Args:
            service (PatientService): The patient service to use for database operations.
            patients_data (list[PatientCreate]): The list of patient data to insert or update.
        """
        inserted_num = 0
        updated_num = 0
        try:
            for patient_data in patients_data:
                existing_patient = service.get_by_patient_code(patient_data.cd_patient)
                if existing_patient:
                    logger.info(f"Updating existing patient: {patient_data.cd_patient}")
                    service.update(existing_patient.id, patient_data)
                    updated_num += 1
                else:
                    logger.info(f"Inserting new patient: {patient_data.cd_patient}")
                    service.create(patient_data)
                    inserted_num += 1
            logger.info(f"Inserted {inserted_num} new patients.")
            logger.info(f"Updated {updated_num} existing patients.")
        except Exception as e:
            logger.error(f"Error inserting or updating patients: {e}")
            raise

    def run(self, year: int | None = None, month: int | None = None) -> None:
        """
        Main method to run the patient import pipeline.

        Args:
            year (int | None, optional): The year for the CSV file. Defaults to None.
            month (int | None, optional): The month for the CSV file. Defaults to None.
        """

        logger.info("PATIENT IMPORT")

        patients_data = self.import_from_csv(year, month)

        with db.session_factory() as session:
            service = PatientService(session)
            self.insert_or_update_patients(service, patients_data)

            total = service.count()
            logger.info(f"Total patients in database: {total}")

        logger.success("IMPORT COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    IngestPatients().run(
        year=2026,
        month=1,
    )
