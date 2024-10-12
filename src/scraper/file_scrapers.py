# src/scraper/file_scrapers.py
import os
import fitz  # PyMuPDF
import docx
from io import BytesIO
from .base_scraper import BaseScraper
from ..document import Document

class PDFScraper(BaseScraper):
    def scrape(self, filepath: str) -> Document:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
            # If page contains images, use OCR
            images = page.get_images()
            for img in images:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha < 4:  # this is GRAY or RGB
                    pix.save("temp_image.png")
                    ocr_text = self.ocr_engine.perform_ocr("temp_image.png")
                    text += ocr_text
                    # Optionally, remove the temporary image file
                    os.remove("temp_image.png")
        doc.close()
        return Document(text, file_path=filepath)  # Pass file_path


class DocxScraper(BaseScraper):
    def scrape(self, filepath: str) -> Document:
        doc = docx.Document(filepath)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return Document('\n'.join(full_text))

class ImageScraper(BaseScraper):
    def scrape(self, filepath: str) -> Document:
        if self.ocr_engine:
            text = self.ocr_engine.perform_ocr(filepath)
            return Document(text)
        else:
            raise ValueError("No OCR engine provided for image scraping.")
