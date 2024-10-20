# src/agents/text_extraction_agent.py

from .base_agent import BaseAgent
from ..utils.logging import Logger


class TextExtractionAgent(BaseAgent):
    def __init__(self, logger: Logger = None):
        self.logger = logger

    def execute(self, document):
        text = document.get_text()
        # Clean up text encoding
        text = text.encode("utf-8", "ignore").decode("utf-8")
        if self.logger:
            self.logger.info("Extracted text from document.")
        return text
