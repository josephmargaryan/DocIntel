# src/scraper/base_scraper.py

import abc
from ..document import Document
from ..ocr_engines.base_ocr import BaseOCREngine


class BaseScraper(abc.ABC):
    """
    Abstract base class for file scrapers.
    """

    def __init__(self, ocr_engine: BaseOCREngine = None):
        self.ocr_engine = ocr_engine

    @abc.abstractmethod
    def scrape(self, filepath: str) -> Document:
        pass
