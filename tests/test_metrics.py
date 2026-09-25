import pytest

from legal_clause_adaptation.evaluation import classification_metrics, holm_adjust


def test_unknown_prediction_is_scored_as_incorrect():
    metrics = classification_metrics(
        ["A", "B", "A"],
        ["A", "Unknown", "B"],
        labels=["A", "B"],
    )
    assert metrics["accuracy"] == pytest.approx(1 / 3)
    assert metrics["unknown_count"] == 1
    assert metrics["unknown_rate"] == pytest.approx(1 / 3)


def test_holm_adjustment_preserves_original_order():
    adjusted = holm_adjust([0.04, 0.01, 0.03])
    assert adjusted.tolist() == pytest.approx([0.06, 0.03, 0.06])
