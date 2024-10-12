# src/ocr_engines/base_ocr.py

import abc

class BaseOCREngine(abc.ABC):
    @abc.abstractmethod
    def perform_ocr(self, image_path: str) -> str:
        pass
