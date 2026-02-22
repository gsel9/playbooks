"""
File input/output helpers and preview utilities.
"""

from pathlib import Path
from typing import Tuple

from config import DATA_FILE_NAME, DATA_PREVIEW_CHARS


def read_data(file_name: str = DATA_FILE_NAME) -> Tuple[str, Path]:
    """Read a text file and return its full contents and path."""
    script_dir = Path(__file__).parent
    file_path = script_dir / file_name
    text = file_path.read_text(encoding="utf-8")
    return text, file_path


def preview_text(text: str, limit: int = DATA_PREVIEW_CHARS) -> str:
    """Return truncated preview of text."""
    return text if len(text) <= limit else f"{text[:limit]}…"
