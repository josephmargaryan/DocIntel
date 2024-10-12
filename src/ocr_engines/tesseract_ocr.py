# src/ocr_engines/tesseract_ocr.py

import pytesseract
from PIL import Image
from .base_ocr import BaseOCREngine

class TesseractOCREngine(BaseOCREngine):
    def perform_ocr(self, image_path: str) -> str:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
