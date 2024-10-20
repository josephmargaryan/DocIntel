# src/utils/misc.py

import os


def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1]
