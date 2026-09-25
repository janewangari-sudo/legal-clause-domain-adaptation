"""Metrics with the study's fixed-label and Unknown-output policy."""

from collections.abc import Sequence

import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def classification_metrics(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    *,
    labels: Sequence[str],
    unknown_label: str = "Unknown",
) -> dict[str, float | int]:
    """Calculate primary metrics over the frozen labels.

    Predictions outside the frozen label list remain incorrect for accuracy and
    receive no class credit in Macro or Weighted F1.
    """
    true_values = np.asarray(y_true, dtype=object)
    predicted_values = np.asarray(y_pred, dtype=object)
    if true_values.shape != predicted_values.shape:
        raise ValueError("True and predicted labels must have equal length")

    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        true_values,
        predicted_values,
        labels=list(labels),
        average="macro",
        zero_division=0,
    )
    _, _, weighted_f1, _ = precision_recall_fscore_support(
        true_values,
        predicted_values,
        labels=list(labels),
        average="weighted",
        zero_division=0,
    )
    unknown_count = int(np.sum(predicted_values == unknown_label))
    return {
        "accuracy": float(accuracy_score(true_values, predicted_values)),
        "macro_precision": float(macro_precision),
        "macro_recall": float(macro_recall),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "unknown_count": unknown_count,
        "unknown_rate": float(unknown_count / len(true_values)) if len(true_values) else 0.0,
    }
