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
        image_paths = []
        # Create a temporary directory specific to this document
        temp_image_dir = os.path.join('temp_images', os.path.splitext(os.path.basename(filepath))[0])
        os.makedirs(temp_image_dir, exist_ok=True)
        for page_num, page in enumerate(doc, start=1):
            text += page.get_text()
            # If page contains images, save them
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image_name = f"image_page{page_num}_{img_index}.png"
                image_path = os.path.join(temp_image_dir, base_image_name)
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha < 4:  # this is GRAY or RGB
                    pix.save(image_path)
                    image_paths.append(image_path)
                    # If we need to perform OCR immediately, we can do it here
                    if self.ocr_engine:
                        ocr_text = self.ocr_engine.perform_ocr(image_path)
                        text += ocr_text
        doc.close()
        return Document(text, file_path=filepath, image_paths=image_paths)

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
            image_paths = [filepath]
            return Document(text, file_path=filepath, image_paths=image_paths)
        else:
            raise ValueError("No OCR engine provided for image scraping.")