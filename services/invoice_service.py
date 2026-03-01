from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core import logger
from models import Invoice
from schemas import InvoiceCreate, InvoiceResponse, InvoiceUpdate

class InvoiceService:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[InvoiceResponse]:
        """
        Retrieves all invoices from the database.

        Returns:
            list[InvoiceResponse]: A list of invoice responses.
        """
        try:
            stmt = select(Invoice).order_by(Invoice.dt_service.desc())
            invoices = self.session.scalars(stmt).all()
            return [InvoiceResponse.model_validate(i) for i in invoices]
        except Exception as e:
            logger.error(f"Error retrieving invoices: {e}")
            raise

    def get_by_id_invoice(self, id_invoice: str) -> InvoiceResponse | None:
        """
        Retrieves an invoice by its ID.

        Args:
            id_invoice (str): The ID of the invoice to search for.

        Returns:
            InvoiceResponse | None: The invoice response if found, otherwise None.
        """
        try:
            stmt = select(Invoice).where(Invoice.id_invoice == id_invoice)
            invoice = self.session.scalars(stmt).first()
            if invoice:
                return InvoiceResponse.model_validate(invoice)
            return None
        except Exception as e:
            logger.error(f"Error retrieving invoice by ID {id_invoice}: {e}")
            raise

    def get_by_cd_patient_cd_procedure(self, cd_patient: str, cd_procedure: str, dt_service: int) -> InvoiceResponse | None:
        """
        Retrieves an invoice by patient code and procedure code.

        Args:
            cd_patient (str): The patient code to search for.
            cd_procedure (str): The procedure code to search for.
            dt_base (int): The reference month and year to search for.

        Returns:
            InvoiceResponse | None: The invoice response if found, otherwise None.
        """
        try:
            stmt = select(Invoice).where(
                Invoice.cd_patient == cd_patient,
                Invoice.cd_procedure == cd_procedure,
                Invoice.dt_service == dt_service
            )
            invoice = self.session.scalars(stmt).first()
            if invoice:
                return InvoiceResponse.model_validate(invoice)
            return None
        except Exception as e:
            logger.error(f"Error retrieving invoice for patient {cd_patient} and procedure {cd_procedure}: {e}")
            raise
    
    def get_by_cd_patient(self, cd_patient: str) -> list[InvoiceResponse]:
        """
        Retrieves all invoices for a given patient.

        Args:
            cd_patient (str): The patient code to search for.

        Returns:
            list[InvoiceResponse]: A list of invoice responses for the given patient.
        """
        try:
            stmt = select(Invoice).where(Invoice.cd_patient == cd_patient)
            invoices = self.session.scalars(stmt).all()
            return [InvoiceResponse.model_validate(i) for i in invoices]
        except Exception as e:
            logger.error(f"Error retrieving invoices for patient {cd_patient}: {e}")
            raise
    
    def count(self) -> int:
        """
        Counts the total number of invoices in the database.

        Returns:
            int: The total count of invoices.
        """
        try:
            stmt = select(func.count(Invoice.id_invoice))
            count = self.session.scalar(stmt)
            return count
        except Exception as e:
            logger.error(f"Error counting invoices: {e}")
            raise

    def create(self, invoice_data: InvoiceCreate) -> InvoiceResponse:
        """
        Creates a new invoice in the database.

        Args:
            invoice_data (InvoiceCreate): The data for the invoice to be created.

        Returns:
            InvoiceResponse: The created invoice response.
        """
        try:
            invoice = Invoice(
                dt_service=invoice_data.dt_service,
                cd_patient=invoice_data.cd_patient,
                cd_procedure=invoice_data.cd_procedure,
                qt_procedure=invoice_data.qt_procedure,
                vl_procedure=invoice_data.vl_procedure,
                nr_page=invoice_data.nr_page,
                dt_base=invoice_data.dt_base,
                nm_file=invoice_data.nm_file
            )
            self.session.add(invoice)
            self.session.commit()
            self.session.refresh(invoice)
            return InvoiceResponse.model_validate(invoice)
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            self.session.rollback()
            raise

    def update(self, id_invoice: str, invoice_data: InvoiceUpdate) -> InvoiceResponse | None:
        """
        Updates an existing invoice in the database.

        Args:
            id_invoice (str): The ID of the invoice to be updated.
            invoice_data (InvoiceUpdate): The data for the invoice to be updated.

        Returns:
            InvoiceResponse | None: The updated invoice response if found and updated, otherwise None.
        """
        try:
            stmt = select(Invoice).where(Invoice.id_invoice == id_invoice)
            invoice = self.session.scalars(stmt).first()
            if not invoice:
                return None
            
            for field, value in invoice_data.model_dump(exclude_unset=True).items():
                setattr(invoice, field, value)
            
            self.session.commit()
            self.session.refresh(invoice)
            return InvoiceResponse.model_validate(invoice)
        except Exception as e:
            logger.error(f"Error updating invoice with ID {id_invoice}: {e}")
            self.session.rollback()
            raise