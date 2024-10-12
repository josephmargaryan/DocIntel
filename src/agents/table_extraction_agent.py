# src/agents/table_extraction_agent.py

import pdfplumber
from .base_agent import BaseAgent
from ..utils.logging import Logger
from ..document import Document

class TableExtractionAgent(BaseAgent):
    def __init__(self, logger: Logger = None):
        self.logger = logger

    def execute(self, document: Document):
        # Check if the document has a file path (required for pdfplumber)
        if not hasattr(document, 'file_path') or not document.file_path.endswith('.pdf'):
            raise ValueError("TableExtractionAgent requires a PDF document with a file_path attribute.")

        tables = []

        try:
            with pdfplumber.open(document.file_path) as pdf:
                for page_number, page in enumerate(pdf.pages, start=1):
                    page_tables = page.extract_tables()
                    for table_number, table in enumerate(page_tables, start=1):
                        if self.logger:
                            self.logger.info(f'Extracted table from page {page_number}, table {table_number}')
                        tables.append({
                            'page': page_number,
                            'table_number': table_number,
                            'data': table
                        })
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error extracting tables: {e}")
            raise e

        return tables
