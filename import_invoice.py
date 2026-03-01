import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pdfplumber

from core import db, logger
from schemas import InvoiceCreate, InvoiceUpdate
from services import InvoiceService, ProcedureService


class IngestInvoiceData:
    def __init__(
        self,
        data_dir: str = "./data",
        file_name: Optional[str] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
    ) -> None:
        self.year, self.month = self._get_dt_base(year, month)
        self.file_pattern = "98663RELATORIO_ATENDIMENTO_{month:02d}_{year}.pdf"
        self.file_name = file_name
        self.dt_base = int(f"{self.year}{self.month:02d}")
        self.data_dir = Path(data_dir)

    @staticmethod
    def _get_dt_base(year: Optional[int], month: Optional[int]) -> Tuple[int, int]:
        """
        Get the base year and month for the invoice data.

        Args:
            year (Optional[int]): The year of the invoice data.
            month (Optional[int]): The month of the invoice data.

        Returns:
            Tuple[int, int]: The base year and month.
        """
        if not year or not month:
            now = datetime.now()
            month = now.month - 1 if now.month > 1 else 12
            year = now.year if month != 12 else now.year - 1
        return year, month

    @property
    def set_file_name(self) -> str:
        """
        Get the file name for the invoice data.

        Returns:
            str: The file name for the invoice data.
        """
        if self.file_name:
            return self.file_name
        return self.file_pattern.format(year=self.year, month=self.month)

    @property
    def file_path(self) -> Path:
        """
        Get the file path for the invoice data.

        Returns:
            Path: The file path for the invoice data.
        """
        return self.data_dir / self.set_file_name

    @staticmethod
    def _extract_service_date(line: str) -> str:
        """
        Extract the service date from a line of text.

        Args:
            line (str): The line of text containing the service date.

        Returns:
            str: The extracted service date in the format DD/MM/YYYY, or None if not found.
        """
        try:
            match = re.match(r"^(\d{2}/\d{2}/\d{4})", line)
            return match.group(1) if match else None
        except Exception as e:
            logger.error(f"Error extracting service date: {e}")
            raise

    @staticmethod
    def _extract_patient_code(line: str) -> str:
        """
        Extract the patient code from a line of text.

        Args:
            line (str): The line of text containing the patient code.

        Returns:
            str: The extracted patient code, or None if not found.
        """
        try:
            match = re.search(r"(\d{4}.\d{2}.\d{5}.\d{2}-\d{1})", line)
            return match.group(1) if match else None
        except Exception as e:
            logger.error(f"Error extracting patient code: {e}")
            raise

    @staticmethod
    def _extract_procedure_code(line: str) -> str:
        """
        Extract the procedure code from a line of text.

        Args:
            line (str): The line of text containing the procedure code.

        Returns:
            str: The extracted procedure code, or None if not found.
        """
        try:
            match = re.search(
                r"\d{1} \d{1} \d{1} \d{1} \d{1} \d{1} \d{2}|\d{1,8}", line
            )
            return match.group(0) if match else None
        except Exception as e:
            logger.error(f"Error extracting procedure code: {e}")
            raise

    @staticmethod
    def _extract_procedure_quantity(line: str) -> int:
        """
        Extract the procedure quantity from a line of text.

        Args:
            line (str): The line of text containing the procedure quantity.

        Returns:
            int: The extracted procedure quantity executed, or None if not found.
        """
        try:
            match = re.search(r"[1-9]{1}", line)
            if match:
                return int(match.group(0).split()[-1])
        except Exception as e:
            logger.error(f"Error extracting procedure quantity: {e}")
            raise

    @staticmethod
    def _extract_values(line: str) -> float:
        """
        Extract the value paid from a line of text.

        Args:
            line (str): The line of text containing the value.

        Returns:
            float: The extracted value, or None if not found.
        """
        try:
            match = re.search(r"\$", line)
            if match:
                line = line[match.span()[1] :]
                numbers = re.findall(r"\d+", line)
                if len(numbers) == 1:
                    value = float(numbers[0])
                elif len(numbers) == 2:
                    value = float(f"{numbers[0]}.{numbers[1]}")
                else:
                    decimals = "".join(numbers[-2:])
                    integers = "".join(numbers[:-2])
                    value = float(f"{integers}.{decimals}")
                return value
            return None
        except Exception as e:
            logger.error(f"Error extracting values: {e}")
            raise

    @staticmethod
    def _find_consulta_procedure(line: str) -> bool:
        """
        Check if the line contains a consulta procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains a consulta procedure, False otherwise.
        """
        try:
            return (
                re.search(r"CONSULTA", line, re.IGNORECASE) is not None
                or re.search(
                    r"\(NO HORÁRIO NORMAL OU PREESTABELECIDO\)", line, re.IGNORECASE
                )
                is not None
            )
        except Exception as e:
            logger.error(f"Error finding consulta procedure: {e}")
            raise

    @staticmethod
    def _find_taxa_sala_procedure(line: str) -> bool:
        """
        Check if the line contains a taxa sala procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains a taxa sala procedure, False otherwise.
        """
        try:
            return (
                re.search(r"TAXA DE SALA", line, re.IGNORECASE) is not None
                or re.search(r"SALA CIRÚRGICA", line, re.IGNORECASE) is not None
                or re.search(r"CIRÚRGICA, PORTE ANESTÉSICO", line, re.IGNORECASE)
                is not None
            )
        except Exception as e:
            logger.error(f"Error finding taxa sala procedure: {e}")
            raise

    @staticmethod
    def _find_biopsia_procedure(line: str) -> bool:
        """
        Check if the line contains a biopsia procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains a biopsia procedure, False otherwise.
        """
        try:
            return (
                re.search(r"BIÓPSIA DE PELE, TUMORES SUPERFICIAIS", line, re.IGNORECASE)
                is not None
                or re.search(r"TECIDO CELULAR SUBCUTÂNEO", line, re.IGNORECASE)
                is not None
            )
        except Exception as e:
            logger.error(f"Error finding biopsia procedure: {e}")
            raise

    @staticmethod
    def _find_cauterizacao_procedure(line: str) -> bool:
        """
        Check if the line contains a cauterizacao procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains a cauterizacao procedure, False otherwise.
        """
        try:
            return re.search(r"CAUTERIZAÇÃO QUÍMICA", line, re.IGNORECASE) is not None
        except Exception as e:
            logger.error(f"Error finding cauterizacao procedure: {e}")
            raise

    @staticmethod
    def _find_criocirurgia_procedure(line: str) -> bool:
        """
        Check if the line contains a criocirurgia procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains a criocirurgia procedure, False otherwise.
        """
        try:
            return (
                re.search(r"CRIOCIRURGIA \(NITROGÊNIO LÍQUIDO\)", line, re.IGNORECASE)
                is not None
            )
        except Exception as e:
            logger.error(f"Error finding criocirurgia procedure: {e}")
            raise

    @staticmethod
    def _find_exerese_procedure(line: str) -> bool:
        """
        Check if the line contains an exerese procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains an exerese procedure, False otherwise.
        """
        try:
            return re.search(r"EXÉRESE TANGENCIAL", line, re.IGNORECASE) is not None
        except Exception as e:
            logger.error(f"Error finding exerese procedure: {e}")
            raise

    @staticmethod
    def _find_infiltracao_procedure(line: str) -> bool:
        """
        Check if the line contains an infiltracao procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains an infiltracao procedure, False otherwise.
        """
        try:
            return (
                re.search(r"INFILTRAÇÃO INTRALESIONAL", line, re.IGNORECASE) is not None
            )
        except Exception as e:
            logger.error(f"Error finding infiltracao procedure: {e}")
            raise

    @staticmethod
    def _find_tu_partes_moles_exerese_procedure(line: str) -> bool:
        """
        Check if the line contains a tu partes moles exerese procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains a tu partes moles exerese procedure, False otherwise.
        """
        try:
            return (
                re.search(r"TU PARTES MOLES - EXÉRESE", line, re.IGNORECASE) is not None
            )
        except Exception as e:
            logger.error(f"Error finding tu partes moles exerese procedure: {e}")
            raise

    @staticmethod
    def _find_exerese_tumor_maligno_procedure(line: str) -> bool:
        """
        Check if the line contains an exerese tumor maligno procedure.

        Args:
            line (str): The line of text to check.

        Returns:
            bool: True if the line contains an exerese tumor maligno procedure, False otherwise.
        """
        try:
            return (
                re.search(r"EXÉRESE DE TUMOR MALIGNO DE PELE", line, re.IGNORECASE)
                is not None
            )
        except Exception as e:
            logger.error(f"Error finding exerese tumor maligno procedure: {e}")
            raise

    @staticmethod
    def _extract_procedures_lines(lines: list[str]) -> list[str]:
        """
        Extract lines that contain procedures based on a date pattern.

        Args:
            lines (list[str]): The list of lines to check.

        Returns:
            list[str]: A list of lines that contain procedures.
        """
        try:
            return [line for line in lines if re.match(r"^\d{2}/\d{2}/\d{4}", line)]
        except Exception as e:
            logger.error(f"Error extracting procedures lines: {e}")
            raise

    @staticmethod
    def _replace_line(line: str, pattern: str) -> str:
        """
        Replace a pattern in a line with an empty string.

        Args:
            line (str): The line of text to modify.
            pattern (str): The pattern to replace.

        Returns:
            str: The modified line.
        """
        try:
            return line.replace(pattern, "").strip()
        except Exception as e:
            logger.error(f"Error replacing line: {e}")
            raise

    def get_procedures_list(self) -> Tuple[List[str], Dict[str, str]]:
        """
        Get the list of procedure codes and a dictionary mapping procedure codes to names.

        Returns:
            Tuple[List[str], Dict[str, str]]: A tuple containing a list of procedure codes and a dictionary mapping procedure codes to names.
        """
        try:
            with db.session_factory() as session:
                procedure_service = ProcedureService(session)
                procedures = procedure_service.get_all()
                procedures_list = [p.cd_procedure for p in procedures]
                procedures_dict = {p.cd_procedure: p.nm_procedure for p in procedures}
            return procedures_list, procedures_dict
        except Exception as e:
            logger.error(f"Error getting procedures list: {e}")
            raise

    def get_code_name_procedure(self, cd_procedure: str, line: str) -> tuple[str, str]:
        """
        Get the procedure code and name based on the extracted code and line content.

        Args:
            cd_procedure (str): The extracted procedure code.
            line (str): The line of text to check.

        Returns:
            tuple[str, str]: A tuple containing the procedure code and name.
        """
        procedures_list, procedures_dict = self.get_procedures_list()
        if cd_procedure not in procedures_list:
            if self._find_consulta_procedure(line):
                cd_procedure = "10101012"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_taxa_sala_procedure(line):
                cd_procedure = "60023090"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_biopsia_procedure(line):
                cd_procedure = "30101077"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_cauterizacao_procedure(line):
                cd_procedure = "30101107"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_criocirurgia_procedure(line):
                cd_procedure = "30101204"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_exerese_procedure(line):
                cd_procedure = "30101506"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_infiltracao_procedure(line):
                cd_procedure = "30101646"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_tu_partes_moles_exerese_procedure(line):
                cd_procedure = "30101913"
                nm_procedure = procedures_dict[cd_procedure]
            elif self._find_exerese_tumor_maligno_procedure(line):
                cd_procedure = "30210119"
                nm_procedure = procedures_dict[cd_procedure]
        else:
            nm_procedure = procedures_dict[cd_procedure]
        return cd_procedure, nm_procedure

    def extract_data(self, line: str) -> Dict[str, str]:
        """
        Extract data from a line of text and return it as a dictionary.

        Args:
            line (str): The line of text to extract data from.

        Returns:
            Dict[str, str]: A dictionary containing the extracted data.
        """
        dt_service = self._extract_service_date(line)
        line_replaced = self._replace_line(line, dt_service)
        dt_service = datetime.strptime(dt_service, "%d/%m/%Y").date()
        cd_patient = self._extract_patient_code(line_replaced)
        line_replaced = self._replace_line(line_replaced, cd_patient)
        cd_procedure = self._extract_procedure_code(line_replaced)
        cd_procedure, nm_procedure = self.get_code_name_procedure(
            cd_procedure, line_replaced
        )
        line_replaced = self._replace_line(line_replaced, cd_procedure)
        line_replaced = self._replace_line(line_replaced, nm_procedure)
        qt_procedure = self._extract_procedure_quantity(line_replaced)
        line_replaced = self._replace_line(line_replaced, str(qt_procedure))
        vl_procedure = self._extract_values(line_replaced)

        return {
            "dt_service": dt_service,
            "cd_patient": cd_patient,
            "cd_procedure": cd_procedure,
            "qt_procedure": qt_procedure,
            "vl_procedure": vl_procedure,
        }

    def get_file_data(self) -> List[Dict[str, str]]:
        """
        Get the data from the PDF file and return it as a list of dictionaries containing the extracted data.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing the extracted data.
        """
        invoice_data = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if not text:
                        continue
                    page_lines = text.split("\n")

                    for line in self._extract_procedures_lines(page_lines):
                        data = self.extract_data(line)
                        data["nr_page"] = page_num
                        data["dt_base"] = self.dt_base
                        data["nm_file"] = self.file_name
                        invoice_data.append(data)
            return invoice_data
        except Exception as e:
            logger.error(f"Error getting PDF data: {e}")
            raise

    def create_nvoice_data(self, data: Dict[str, str]) -> InvoiceCreate:
        """
        Create an InvoiceCreate object from the extracted data.

        Args:
            data (Dict[str, str]): The extracted data to create the InvoiceCreate object from.

        Returns:
            InvoiceCreate: The created InvoiceCreate object.
        """
        try:
            return InvoiceCreate(**data)
        except Exception as e:
            logger.error(f"Error creating InvoiceCreate object: {e}")
            raise

    def insert_or_update_invoices(
        self, service: InvoiceService, invoices_data: List[InvoiceCreate]
    ) -> None:
        inserted_num = 0
        updated_num = 0
        try:
            for invoice_data in invoices_data:
                existing_invoice = service.get_by_cd_patient_cd_procedure(
                    invoice_data.cd_patient,
                    invoice_data.cd_procedure,
                    invoice_data.dt_service,
                )
                if existing_invoice:
                    logger.info(
                        f"Updating existing invoice: {existing_invoice.id_invoice}"
                    )
                    service.update(
                        existing_invoice.id_invoice,
                        InvoiceUpdate(**invoice_data.model_dump()),
                    )
                    updated_num += 1
                else:
                    logger.info(
                        f"Inserting new invoice for patient {invoice_data.cd_patient} and procedure {invoice_data.cd_procedure}"
                    )
                    service.create(invoice_data)
                    inserted_num += 1
            logger.info(f"Inserted {inserted_num} new invoices")
            logger.info(f"Updated {updated_num} existing invoices")
        except Exception as e:
            logger.error(f"Error inserting or updating invoices: {e}")
            raise

    def run(self) -> None:
        """
        Run the data ingestion process for the specified year and month.

        Args:
            year (int | None): The year of the invoice data to ingest. If None, defaults to the previous month.
            month (int | None): The month of the invoice data to ingest. If None, defaults to the previous month.
        """
        logger.info("INVOICE DATA INGESTION STARTED")

        invoice_data = self.get_file_data()
        invoices_create = [self.create_nvoice_data(data) for data in invoice_data]

        with db.session_factory() as session:
            invoice_service = InvoiceService(session)
            self.insert_or_update_invoices(invoice_service, invoices_create)

            total_invoices = invoice_service.count()
            logger.info(f"Total invoices in the database: {total_invoices}")

        logger.success("INVOICE DATA INGESTION COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    IngestInvoiceData(year=2026, month=1)
