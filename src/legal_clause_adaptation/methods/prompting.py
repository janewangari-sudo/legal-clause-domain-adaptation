"""Prompt construction and conservative generated-label parsing."""

from collections.abc import Sequence


def build_classification_instruction(clause_text: str, labels: Sequence[str]) -> str:
    """Build a deterministic fixed-label classification instruction."""
    label_text = ", ".join(labels)
    return (
        "Classify the legal contract clause into exactly one allowed label.\n"
        f"Allowed labels: {label_text}\n\n"
        f"Clause:\n{clause_text.strip()}\n\n"
        "Return only the label."
    )


def parse_generated_label(
    generated_text: str, labels: Sequence[str], *, unknown_label: str = "Unknown"
) -> str:
    """Accept only one exact canonical label after minimal whitespace cleanup."""
    candidate = generated_text.strip().strip("`\"'").strip()
    return candidate if candidate in set(labels) else unknown_label
