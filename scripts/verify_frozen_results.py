"""Verify the published frozen predictions without datasets or model weights."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from legal_clause_adaptation import FROZEN_LABELS

ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS = ROOT / "results" / "predictions"
METADATA = ROOT / "results" / "metadata"
UNKNOWN = "Unknown"

METHOD_COLUMNS = (
    "TF-IDF + Logistic Regression",
    "Zero-shot",
    "Original PEFT",
    "RAG",
    "Hybrid",
    "Corrected PEFT (post-hoc)",
)


def check_row_ids(frame: pd.DataFrame, expected_rows: int, name: str) -> None:
    if len(frame) != expected_rows:
        raise ValueError(f"{name}: expected {expected_rows} rows, found {len(frame)}")
    if not frame["row_id"].is_unique:
        raise ValueError(f"{name}: row_id is not unique")
    if set(frame["row_id"]) != set(range(expected_rows)):
        raise ValueError(f"{name}: row_id is not the complete zero-based row set")


def metrics(frame: pd.DataFrame) -> dict[str, float | int]:
    true = frame["clause_type"]
    predicted = frame["predicted_label"]
    return {
        "accuracy": accuracy_score(true, predicted),
        "macro_precision": precision_score(
            true, predicted, labels=FROZEN_LABELS, average="macro", zero_division=0
        ),
        "macro_recall": recall_score(
            true, predicted, labels=FROZEN_LABELS, average="macro", zero_division=0
        ),
        "macro_f1": f1_score(
            true, predicted, labels=FROZEN_LABELS, average="macro", zero_division=0
        ),
        "weighted_f1": f1_score(
            true, predicted, labels=FROZEN_LABELS, average="weighted", zero_division=0
        ),
        "unknown_count": int(predicted.eq(UNKNOWN).sum()),
    }


def assert_close(actual: float, expected: float, name: str) -> None:
    if abs(actual - expected) > 1e-12:
        raise ValueError(f"{name}: expected {expected!r}, found {actual!r}")


def main() -> None:
    validation = pd.read_csv(PREDICTIONS / "corrected_peft_validation_predictions.csv")
    test = pd.read_csv(PREDICTIONS / "corrected_peft_test_predictions.csv")
    six = pd.read_csv(PREDICTIONS / "six_method_test_predictions.csv")
    check_row_ids(validation, 833, "corrected PEFT validation predictions")
    check_row_ids(test, 1850, "corrected PEFT test predictions")
    check_row_ids(six, 1850, "six-method test predictions")

    allowed = set(FROZEN_LABELS) | {UNKNOWN}
    for name, frame, columns in (
        ("validation", validation, ("clause_type", "predicted_label")),
        ("test", test, ("clause_type", "predicted_label")),
        ("six-method", six, ("clause_type", *METHOD_COLUMNS)),
    ):
        for column in columns:
            unexpected = set(frame[column].dropna()) - allowed
            if unexpected:
                raise ValueError(f"{name}/{column}: unexpected labels {sorted(unexpected)}")

    if six["group_id"].nunique() != 57:
        raise ValueError("Six-method predictions do not contain 57 anonymous groups")
    if not six["group_id"].str.fullmatch(r"group_\d{3}").all():
        raise ValueError("Anonymous group identifiers have an unexpected format")
    if not six["clause_type"].equals(test["clause_type"]):
        raise ValueError("Six-method and corrected PEFT test labels are not aligned")
    if not six["Corrected PEFT (post-hoc)"].equals(test["predicted_label"]):
        raise ValueError("Published corrected PEFT predictions are inconsistent")

    expected_test = json.loads(
        (METADATA / "corrected_peft_test_metrics.json").read_text(encoding="utf-8")
    )
    actual_test = metrics(test)
    for key in ("accuracy", "macro_precision", "macro_recall", "macro_f1", "weighted_f1"):
        assert_close(float(actual_test[key]), float(expected_test[key]), f"test {key}")
    if actual_test["unknown_count"] != expected_test["unknown_count"]:
        raise ValueError("Corrected PEFT test unknown count changed")

    expected_validation = {
        "accuracy": 0.9255702280912363,
        "macro_precision": 0.8726878178607113,
        "macro_recall": 0.851627497826653,
        "macro_f1": 0.854972291860513,
        "weighted_f1": 0.9212239613050025,
        "unknown_count": 0,
    }
    actual_validation = metrics(validation)
    for key in ("accuracy", "macro_precision", "macro_recall", "macro_f1", "weighted_f1"):
        assert_close(
            float(actual_validation[key]), float(expected_validation[key]), f"validation {key}"
        )
    if actual_validation["unknown_count"] != expected_validation["unknown_count"]:
        raise ValueError("Corrected PEFT validation unknown count changed")

    primary = pd.read_csv(ROOT / "results" / "tables" / "primary_metrics.csv")
    method_aliases = {"Original PEFT": "PEFT"}
    for method in METHOD_COLUMNS:
        predictions = six[method]
        true = six["clause_type"]
        accuracy = accuracy_score(true, predictions)
        macro_f1 = f1_score(
            true, predictions, labels=FROZEN_LABELS, average="macro", zero_division=0
        )
        if method == "Corrected PEFT (post-hoc)":
            assert_close(accuracy, expected_test["accuracy"], f"{method} accuracy")
            assert_close(macro_f1, expected_test["macro_f1"], f"{method} macro F1")
            continue
        table_name = method_aliases.get(method, method)
        row = primary.loc[primary["method"].eq(table_name)]
        if len(row) != 1:
            raise ValueError(f"Missing aggregate result for {method}")
        if round(accuracy, 4) != float(row.iloc[0]["accuracy"]):
            raise ValueError(f"{method}: row-level accuracy differs from the published table")
        if round(macro_f1, 4) != float(row.iloc[0]["macro_f1"]):
            raise ValueError(f"{method}: row-level Macro F1 differs from the published table")

    forbidden_columns = {"clause_text", "raw_output", "contract_title"}
    for path in PREDICTIONS.glob("*.csv"):
        columns = set(pd.read_csv(path, nrows=0).columns)
        leaked = columns & forbidden_columns
        if leaked:
            raise ValueError(f"{path}: contains private columns {sorted(leaked)}")
    for path in METADATA.glob("*.json"):
        if "/content/drive" in path.read_text(encoding="utf-8"):
            raise ValueError(f"{path}: contains an account-specific Google Drive path")

    print("Frozen public results verified.")
    print(
        "Corrected PEFT test: "
        f"accuracy={actual_test['accuracy']:.4f}, "
        f"macro_f1={actual_test['macro_f1']:.4f}, "
        f"rows={len(test)}, groups={six['group_id'].nunique()}"
    )


if __name__ == "__main__":
    main()
