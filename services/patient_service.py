from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core import logger
from models import Patient
from schemas import PatientCreate, PatientResponse


class PatientService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[PatientResponse]:
        """
        Retrieves all patients from the database.

        Returns:
            list[PatientResponse]: A list of patient responses.
        """
        try:
            stmt = select(Patient).order_by(Patient.nm_patient)
            patients = self.session.scalars(stmt).all()
            return [PatientResponse.model_validate(p) for p in patients]
        except Exception as e:
            logger.error(f"Error retrieving patients: {e}")
            raise

    def get_by_patient_code(self, patient_code: str) -> PatientResponse | None:
        """
        Retrieves a patient by their patient code.

        Args:
            patient_code (str): The patient code to search for.

        Returns:
            PatientResponse | None: The patient response if found, otherwise None.
        """
        try:
            patient = self.session.get(Patient, patient_code)
            if patient:
                return PatientResponse.model_validate(patient)
            return None
        except Exception as e:
            logger.error(f"Error retrieving patient by code: {e}")
            raise

    def count(self) -> int:
        """
        Returns the total number of patients.

        Returns:
            int: The total number of patients.
        """
        try:
            return self.session.scalar(select(func.count(Patient.cd_patient)))
        except Exception as e:
            logger.error(f"Error counting patients: {e}")
            raise

    def create(self, patient_data: PatientCreate) -> PatientResponse:
        """
        Creates a new patient in the database.

        Args:
            patient_data (PatientCreate): The data for the patient to be created.

        Returns:
            PatientResponse: The created patient response.
        """
        try:
            patient = Patient(
                cd_patient=patient_data.cd_patient,
                nm_patient=patient_data.nm_patient,
                ds_address=patient_data.ds_address,
            )
            self.session.add(patient)
            self.session.commit()
            self.session.refresh(patient)
            return PatientResponse.model_validate(patient)
        except Exception as e:
            logger.error(f"Error creating patient: {e}")
            raise

    def update(
        self, patient_code: str, patient_data: PatientCreate
    ) -> PatientResponse:
        """
        Updates an existing patient.

        Args:
            patient_code (str): The patient code of the patient to update.
            patient_data (PatientCreate): The data for the patient to be updated.

        Returns:
            PatientResponse: The updated patient response.
        """
        try:
            patient = self.session.get(Patient, patient_code)
            if not patient:
                raise ValueError(f"Patient with code {patient_code} not found")

            patient.cd_patient = patient_data.cd_patient
            patient.nm_patient = patient_data.nm_patient
            patient.ds_address = patient_data.ds_address

            self.session.commit()
            self.session.refresh(patient)
            return PatientResponse.model_validate(patient)
        except Exception as e:
            logger.error(f"Error updating patient: {e}")
            raise
