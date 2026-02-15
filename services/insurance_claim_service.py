from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core import logger
from models import InsuranceClaim
from schemas import InsuranceClaimCreate, InsuranceClaimResponse, InsuranceClaimUpdate


class InsuranceClaimService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[InsuranceClaimResponse]:
        """
        Retrieves all insurance claims from the database.

        Returns:
            list[InsuranceClaimResponse]: A list of insurance claim responses.
        """
        try:
            stmt = select(InsuranceClaim).order_by(InsuranceClaim.dm_service.desc())
            claims = self.session.scalars(stmt).all()
            return [InsuranceClaimResponse.model_validate(c) for c in claims]
        except Exception as e:
            logger.error(f"Error retrieving insurance claims: {e}")
            raise

    def get_by_claim_number(self, nr_claim: str) -> InsuranceClaimResponse | None:
        """
        Retrieves an insurance claim by its claim number.

        Args:
            nr_claim (str): The claim number to search for.

        Returns:
            InsuranceClaimResponse | None: The claim response if found, otherwise None.
        """
        try:
            claim = self.session.get(InsuranceClaim, nr_claim)
            if claim:
                return InsuranceClaimResponse.model_validate(claim)
            return None
        except Exception as e:
            logger.error(f"Error retrieving insurance claim by number: {e}")
            raise

    def get_by_patient_code(self, cd_patient: str) -> list[InsuranceClaimResponse]:
        """
        Retrieves all insurance claims for a given patient.

        Args:
            cd_patient (str): The patient code to search for.

        Returns:
            list[InsuranceClaimResponse]: A list of claim responses for the patient.
        """
        try:
            stmt = (
                select(InsuranceClaim)
                .where(InsuranceClaim.cd_patient == cd_patient)
                .order_by(InsuranceClaim.dm_service.desc())
            )
            claims = self.session.scalars(stmt).all()
            return [InsuranceClaimResponse.model_validate(c) for c in claims]
        except Exception as e:
            logger.error(f"Error retrieving insurance claims by patient: {e}")
            raise

    def count(self) -> int:
        """
        Returns the total number of insurance claims.

        Returns:
            int: The total number of insurance claims.
        """
        try:
            return self.session.scalar(select(func.count(InsuranceClaim.nr_claim)))
        except Exception as e:
            logger.error(f"Error counting insurance claims: {e}")
            raise

    def create(self, claim_data: InsuranceClaimCreate) -> InsuranceClaimResponse:
        """
        Creates a new insurance claim in the database.

        Args:
            claim_data (InsuranceClaimCreate): The data for the claim to be created.

        Returns:
            InsuranceClaimResponse: The created claim response.
        """
        try:
            claim = InsuranceClaim(
                nr_claim=claim_data.nr_claim,
                nr_request=claim_data.nr_request,
                cd_patient=claim_data.cd_patient,
                dt_issue=claim_data.dt_issue,
                dm_service=claim_data.dm_service,
                st_claim=claim_data.st_claim,
                tp_claim=claim_data.tp_claim,
                fg_return=claim_data.fg_return,
                cd_procedure=claim_data.cd_procedure,
                nm_procedure=claim_data.nm_procedure,
                qt_procedure=claim_data.qt_procedure,
            )
            self.session.add(claim)
            self.session.commit()
            self.session.refresh(claim)
            return InsuranceClaimResponse.model_validate(claim)
        except Exception as e:
            logger.error(f"Error creating insurance claim: {e}")
            raise

    def update(
        self, nr_claim: str, claim_data: InsuranceClaimUpdate
    ) -> InsuranceClaimResponse:
        """
        Updates an existing insurance claim.

        Args:
            nr_claim (str): The claim number of the claim to update.
            claim_data (InsuranceClaimUpdate): The data to update.

        Returns:
            InsuranceClaimResponse: The updated claim response.
        """
        try:
            claim = self.session.get(InsuranceClaim, nr_claim)
            if not claim:
                raise ValueError(f"Insurance claim with number {nr_claim} not found")

            update_data = claim_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(claim, field, value)

            self.session.commit()
            self.session.refresh(claim)
            return InsuranceClaimResponse.model_validate(claim)
        except Exception as e:
            logger.error(f"Error updating insurance claim: {e}")
            raise
