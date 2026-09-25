from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_primary_metrics_match_frozen_summary():
    metrics = pd.read_csv(ROOT / "results/tables/primary_metrics.csv").set_index("method")
    assert metrics.loc["TF-IDF + Logistic Regression", "accuracy"] == 0.8605
    assert metrics.loc["TF-IDF + Logistic Regression", "macro_f1"] == 0.8131
    assert metrics.loc["RAG", "macro_f1"] == 0.7762
    assert metrics.loc["Hybrid", "macro_f1"] == 0.7764
    assert metrics.loc["Zero-shot", "unknown_count"] == 244
