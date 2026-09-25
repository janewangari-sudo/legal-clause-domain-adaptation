"""Grouped splitting utilities using annotated document-title values."""

from collections.abc import Mapping

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


def split_by_document_title(
    dataframe: pd.DataFrame,
    *,
    group_column: str = "contract_title",
    random_seed: int = 42,
    test_size: float = 0.2,
    validation_fraction_of_remainder: float = 0.15,
) -> dict[str, pd.DataFrame]:
    """Reproduce the two-stage grouped split used in the primary study."""
    if group_column not in dataframe:
        raise ValueError(f"Missing grouping column: {group_column}")

    first_split = GroupShuffleSplit(
        n_splits=1, test_size=test_size, random_state=random_seed
    )
    train_validation_index, test_index = next(
        first_split.split(dataframe, groups=dataframe[group_column])
    )
    train_validation = dataframe.iloc[train_validation_index].reset_index(drop=True)
    test = dataframe.iloc[test_index].reset_index(drop=True)

    second_split = GroupShuffleSplit(
        n_splits=1,
        test_size=validation_fraction_of_remainder,
        random_state=random_seed,
    )
    train_index, validation_index = next(
        second_split.split(train_validation, groups=train_validation[group_column])
    )
    splits = {
        "train": train_validation.iloc[train_index].reset_index(drop=True),
        "validation": train_validation.iloc[validation_index].reset_index(drop=True),
        "test": test,
    }
    validate_group_separation(splits, group_column=group_column)
    return splits


def validate_group_separation(
    splits: Mapping[str, pd.DataFrame], *, group_column: str = "contract_title"
) -> None:
    """Raise when an annotated document-title group crosses split boundaries."""
    required = {"train", "validation", "test"}
    if set(splits) != required:
        raise ValueError(f"Expected split names {sorted(required)}, received {sorted(splits)}")

    groups = {
        name: set(frame[group_column].dropna().astype(str)) for name, frame in splits.items()
    }
    pairs = (("train", "validation"), ("train", "test"), ("validation", "test"))
    overlaps = {
        f"{left}-{right}": groups[left] & groups[right]
        for left, right in pairs
        if groups[left] & groups[right]
    }
    if overlaps:
        counts = {pair: len(values) for pair, values in overlaps.items()}
        raise ValueError(f"Document-title-group overlap detected: {counts}")
