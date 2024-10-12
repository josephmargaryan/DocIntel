# src/scraper/ocr.py

from PIL import Image
from ..ocr_engines.base_ocr import BaseOCREngine

class OCRProcessor:
    def __init__(self, ocr_engine: BaseOCREngine):
        self.ocr_engine = ocr_engine

    def process_image(self, image_path: str) -> str:
        return self.ocr_engine.perform_ocr(image_path)
