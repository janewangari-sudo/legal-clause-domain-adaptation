"""Text transformations used by the data-preparation workflow."""

import re


def clean_clause_text(text: object) -> str:
    """Strip surrounding whitespace while preserving case and legal punctuation."""
    return str(text).strip()


def normalize_for_duplicate(text: object) -> str:
    """Return the diagnostic normal form used for exact duplicate auditing."""
    return re.sub(r"\s+", " ", clean_clause_text(text).casefold())
