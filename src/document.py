# src/document.py


class Document:
    """
    Represents a scraped document.
    """

    def __init__(
        self,
        text: str,
        file_path: str = None,
        image_paths: list = None,
        rows: list = None,
    ):
        """
        Initializes the Document object.

        Parameters:
        - text (str): The extracted text from the document.
        - file_path (str): The file path of the document.
        - image_paths (list): List of image paths related to the document (if applicable).
        - rows (list): List of rows for structured data (for Excel or table extraction).
        """
        self.text = text
        self.file_path = file_path
        self.image_paths = image_paths if image_paths else []
        self.rows = rows if rows else []  # Add support for rows

    def get_text(self) -> str:
        return self.text
