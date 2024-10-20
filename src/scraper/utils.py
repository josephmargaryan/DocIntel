# src/scraper/utils.py

import re


def clean_text(text: str) -> str:
    """
    Cleans up text using regular expressions.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()
