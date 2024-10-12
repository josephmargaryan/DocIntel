# src/document.py

class Document:
    """
    Represents a scraped document.
    """

    def __init__(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text
