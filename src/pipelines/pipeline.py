# src/pipelines/pipeline.py

from ..scraper.file_scrapers import PDFScraper, DocxScraper, ImageScraper
from ..ocr_engines.tesseract_ocr import TesseractOCREngine

class DocumentProcessingPipeline:
    def __init__(self):
        self.ocr_engine = TesseractOCREngine()
        self.pdf_scraper = PDFScraper(ocr_engine=self.ocr_engine)
        self.docx_scraper = DocxScraper()
        self.image_scraper = ImageScraper(ocr_engine=self.ocr_engine)

    def process(self, filepath: str):
        if filepath.endswith('.pdf'):
            document = self.pdf_scraper.scrape(filepath)
        elif filepath.endswith('.docx'):
            document = self.docx_scraper.scrape(filepath)
        elif filepath.endswith(('.png', '.jpg', '.jpeg')):
            document = self.image_scraper.scrape(filepath)
        else:
            raise ValueError("Unsupported file format.")
        return document
