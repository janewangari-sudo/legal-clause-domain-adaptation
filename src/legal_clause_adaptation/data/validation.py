"""Schema and frozen-split validation."""

from collections.abc import Mapping, Sequence

import pandas as pd

from legal_clause_adaptation.constants import REQUIRED_COLUMNS
from legal_clause_adaptation.data.splitting import validate_group_separation


def validate_dataframe(
    dataframe: pd.DataFrame,
    *,
    labels: Sequence[str],
    split_name: str,
) -> None:
    """Validate required columns, nulls, and frozen class membership."""
    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"{split_name} is missing columns: {sorted(missing_columns)}")
    if dataframe[["clause_text", "clause_type", "contract_title"]].isna().any().any():
        raise ValueError(f"{split_name} contains missing required values")

    observed = set(dataframe["clause_type"].astype(str))
    expected = set(labels)
    unknown = sorted(observed - expected)
    missing = sorted(expected - observed)
    if unknown or missing:
        raise ValueError(
            f"{split_name} label schema differs from the frozen schema; "
            f"unknown={unknown}, missing={missing}"
        )


def validate_split_collection(
    splits: Mapping[str, pd.DataFrame],
    *,
    labels: Sequence[str],
    expected_sizes: Mapping[str, int] | None = None,
) -> None:
    """Validate every split and ensure document-title-group separation."""
    for name, dataframe in splits.items():
        validate_dataframe(dataframe, labels=labels, split_name=name)
    if expected_sizes is not None:
        observed_sizes = {name: len(frame) for name, frame in splits.items()}
        if observed_sizes != dict(expected_sizes):
            raise ValueError(
                f"Frozen split sizes changed; expected={dict(expected_sizes)}, "
                f"observed={observed_sizes}"
            )
    validate_group_separation(splits)
