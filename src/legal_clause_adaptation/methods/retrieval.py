"""Formatting helpers for RAG demonstrations."""

from collections.abc import Iterable, Mapping


def format_retrieved_examples(examples: Iterable[Mapping[str, str]]) -> str:
    """Format retrieved training clauses as labelled prompt demonstrations."""
    blocks = []
    for index, example in enumerate(examples, start=1):
        blocks.append(
            f"Example {index}\n"
            f"Clause: {example['clause_text'].strip()}\n"
            f"Label: {example['clause_type'].strip()}"
        )
    return "\n\n".join(blocks)
