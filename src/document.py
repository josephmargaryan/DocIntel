# src/document.py

class Document:
    """
    Represents a scraped document.
    """

    def __init__(self, text: str, file_path: str = None, image_paths: list = None):
        self.text = text
        self.file_path = file_path
        self.image_paths = image_paths if image_paths else []

    def get_text(self) -> str:
        return self.text
