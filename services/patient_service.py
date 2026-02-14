from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import Patient
from schemas import PatientCreate, PatientResponse


class PatientService:
    """Service for managing patient operations."""

    DATA_DIR = Path("./data")
    FILE_PATTERN = "{year}{month:02d}_atendimentos_sao_lucas.csv"

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[PatientResponse]:
        """Returns all patients ordered by name."""
        stmt = select(Patient).order_by(Patient.nm_patiente)
        patients = self.session.scalars(stmt).all()
        return [PatientResponse.model_validate(p) for p in patients]

    def get_by_codigo(self, codigo: str) -> PatientResponse | None:
        """Finds a patient by their code."""
        stmt = select(Patient).where(Patient.cd_patiente == codigo)
        patient = self.session.scalars(stmt).first()
        if patient:
            return PatientResponse.model_validate(patient)
        return None

    def get_by_id(self, patient_id: int) -> PatientResponse | None:
        """Finds a patient by their ID."""
        patient = self.session.get(Patient, patient_id)
        if patient:
            return PatientResponse.model_validate(patient)
        return None

    def count(self) -> int:
        """Returns the total number of patients."""
        return self.session.scalar(select(func.count(Patient.id)))

    def create(self, patient_data: PatientCreate) -> PatientResponse:
        """Creates a new patient."""
        patient = Patient(
            cd_patiente=patient_data.cd_patiente,
            nm_patiente=patient_data.nm_patiente,
            ds_endereco=patient_data.ds_endereco,
        )
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)
        return PatientResponse.model_validate(patient)

    def upsert(self, patient_data: PatientCreate) -> tuple[PatientResponse, bool]:
        """
        Creates or updates a patient based on cd_patiente.
        Returns tuple of (patient, was_inserted).
        """
        existing = self.session.execute(
            select(Patient).where(Patient.cd_patiente == patient_data.cd_patiente)
        ).scalar_one_or_none()

        stmt = insert(Patient).values(
            cd_patiente=patient_data.cd_patiente,
            nm_patiente=patient_data.nm_patiente,
            ds_endereco=patient_data.ds_endereco,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["cd_patiente"],
            set_={
                "nm_patiente": stmt.excluded.nm_patiente,
                "ds_endereco": stmt.excluded.ds_endereco,
            },
        ).returning(Patient)

        result = self.session.execute(stmt)
        patient = result.scalar_one()
        self.session.commit()

        was_inserted = existing is None
        return PatientResponse.model_validate(patient), was_inserted

    def _get_csv_path(self, year: int | None = None, month: int | None = None) -> Path:
        """Builds the CSV file path for the given year and month."""
        now = datetime.now()
        year = year or now.year
        month = month or now.month

        filename = self.FILE_PATTERN.format(year=year, month=month)
        return self.DATA_DIR / filename

    def import_from_csv(
        self, year: int | None = None, month: int | None = None
    ) -> tuple[int, int]:
        """
        Imports patients from the CSV file for the given year/month.
        Uses current year/month if not specified.
        Returns tuple of (inserted_count, updated_count).
        """
        csv_path = self._get_csv_path(year, month)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        print(f"Reading file: {csv_path}")

        df = pd.read_csv(csv_path, encoding="utf-8-sig")

        # Extract unique patients
        patients_df = df[
            ["Cd Beneficiário", "Beneficiário", "Endereço Beneficiário"]
        ].copy()
        patients_df.columns = ["cd_patiente", "nm_patiente", "ds_endereco"]

        # Remove duplicates keeping first occurrence
        patients_df = patients_df.drop_duplicates(subset="cd_patiente", keep="first")

        # Clean data
        patients_df["nm_patiente"] = patients_df["nm_patiente"].str.strip()
        patients_df["ds_endereco"] = patients_df["ds_endereco"].str.strip()
        patients_df["cd_patiente"] = patients_df["cd_patiente"].str.strip()

        inserted_count = 0
        updated_count = 0

        for _, row in patients_df.iterrows():
            patient_data = PatientCreate(
                cd_patiente=row["cd_patiente"],
                nm_patiente=row["nm_patiente"],
                ds_endereco=row["ds_endereco"],
            )

            _, was_inserted = self.upsert(patient_data)

            if was_inserted:
                inserted_count += 1
            else:
                updated_count += 1

        print(f"Patients inserted: {inserted_count}")
        print(f"Patients updated: {updated_count}")
        print(f"Total processed: {inserted_count + updated_count}")

        return inserted_count, updated_count
