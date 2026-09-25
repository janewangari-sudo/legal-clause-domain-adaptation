"""Paired comparison helpers used by the final analysis."""

from collections.abc import Sequence

import numpy as np
from scipy.stats import binomtest


def holm_adjust(p_values: Sequence[float]) -> np.ndarray:
    """Return Holm step-down adjusted p-values in their original order."""
    values = np.asarray(p_values, dtype=float)
    order = np.argsort(values)
    adjusted = np.empty(len(values), dtype=float)
    running_maximum = 0.0
    for rank, original_index in enumerate(order):
        corrected = min(1.0, (len(values) - rank) * values[original_index])
        running_maximum = max(running_maximum, corrected)
        adjusted[original_index] = running_maximum
    return adjusted


def exact_mcnemar(
    y_true: Sequence[str], predictions_a: Sequence[str], predictions_b: Sequence[str]
) -> dict[str, int | float]:
    """Calculate the exact two-sided McNemar test for paired predictions."""
    truth = np.asarray(y_true, dtype=object)
    first = np.asarray(predictions_a, dtype=object)
    second = np.asarray(predictions_b, dtype=object)
    if not (truth.shape == first.shape == second.shape):
        raise ValueError("Truth and both prediction arrays must have equal shape")
    first_correct = first == truth
    second_correct = second == truth
    first_only = int(np.sum(first_correct & ~second_correct))
    second_only = int(np.sum(~first_correct & second_correct))
    discordant = first_only + second_only
    p_value = 1.0 if discordant == 0 else float(
        binomtest(first_only, discordant, p=0.5, alternative="two-sided").pvalue
    )
    return {
        "a_only_correct": first_only,
        "b_only_correct": second_only,
        "discordant_pairs": discordant,
        "raw_p_value": p_value,
    }
