from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core import logger
from models import Procedure
from schemas import ProcedureCreate, ProcedureResponse


class ProcedureService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[ProcedureResponse]:
        """
        Retrieves all procedures from the database.

        Returns:
            list[ProcedureResponse]: A list of procedure responses.
        """
        try:
            stmt = select(Procedure).order_by(Procedure.nm_procedure)
            procedures = self.session.scalars(stmt).all()
            return [ProcedureResponse.model_validate(p) for p in procedures]
        except Exception as e:
            logger.error(f"Error retrieving procedures: {e}")
            raise

    def count(self) -> int:
        """
        Returns the total number of procedures.

        Returns:
            int: The total number of procedures.
        """
        try:
            return self.session.scalar(select(func.count(Procedure.cd_procedure)))
        except Exception as e:
            logger.error(f"Error counting procedures: {e}")
            raise

    def create(self, procedure_data: ProcedureCreate) -> ProcedureResponse:
        """
        Creates a new procedure in the database.

        Args:
            procedure_data (ProcedureCreate): The data for the new procedure.

        Returns:
            ProcedureResponse: The created procedure response.
        """
        try:
            procedure = Procedure(**procedure_data.model_dump())
            self.session.add(procedure)
            self.session.commit()
            self.session.refresh(procedure)
            return ProcedureResponse.model_validate(procedure)
        except Exception as e:
            logger.error(f"Error creating procedure: {e}")
            self.session.rollback()
            raise
