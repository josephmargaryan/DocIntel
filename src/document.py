# src/document.py

class Document:
    """
    Represents a scraped document.
    """

    def __init__(self, text: str, file_path: str = None):
        self.text = text
        self.file_path = file_path  # Add file_path attribute

    def get_text(self) -> str:
        return self.text

