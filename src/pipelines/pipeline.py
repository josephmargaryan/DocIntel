# src/pipelines/pipeline.py

from ..scraper.file_scrapers import PDFScraper, DocxScraper, ImageScraper, ExcelScraper
from ..ocr_engines.tesseract_ocr import TesseractOCREngine

# src/pipelines/pipeline.py


class DocumentProcessingPipeline:
    def __init__(self):
        self.ocr_engine = TesseractOCREngine()  # For image OCR
        self.pdf_scraper = PDFScraper(ocr_engine=self.ocr_engine)
        self.docx_scraper = DocxScraper()
        self.image_scraper = ImageScraper(ocr_engine=self.ocr_engine)
        self.excel_scraper = ExcelScraper()  # Add ExcelScraper here

    def process(self, filepath: str):
        if filepath.endswith(".pdf"):
            document = self.pdf_scraper.scrape(filepath)
        elif filepath.endswith(".docx"):
            document = self.docx_scraper.scrape(filepath)
        elif filepath.endswith((".png", ".jpg", ".jpeg")):
            document = self.image_scraper.scrape(filepath)
        elif filepath.endswith(".xlsx"):
            document = self.excel_scraper.scrape(filepath)  # Excel processing
        else:
            raise ValueError("Unsupported file format.")
        return document
