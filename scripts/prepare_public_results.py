"""Create privacy-safe public artifacts from the frozen experiment outputs.

This script is not required to verify the published files. It documents the
one-way sanitization applied before row-level results are committed. Run it
only against the private project directory that contains the original files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def read_csv(path: Path, expected_rows: int) -> pd.DataFrame:
    frame = pd.read_csv(path)
    if len(frame) != expected_rows:
        raise ValueError(f"{path.name}: expected {expected_rows} rows, found {len(frame)}")
    return frame


def write_predictions(
    source: Path,
    destination: Path,
    expected_rows: int,
) -> pd.DataFrame:
    frame = read_csv(source, expected_rows)
    required = {"row_id", "clause_type", "predicted_label"}
    if not required.issubset(frame.columns):
        raise ValueError(f"{source.name}: missing columns {sorted(required - set(frame.columns))}")
    public = frame[["row_id", "clause_type", "predicted_label"]].copy()
    public.to_csv(destination, index=False)
    return frame


def main() -> None:
    args = parse_args()
    private = args.private_dir.resolve()
    output = args.output_dir.resolve()
    predictions = output / "predictions"
    metadata = output / "metadata"
    predictions.mkdir(parents=True, exist_ok=True)
    metadata.mkdir(parents=True, exist_ok=True)

    validation = write_predictions(
        private / "peft_v4_validation_training_prompt_single_bos_final.csv",
        predictions / "corrected_peft_validation_predictions.csv",
        833,
    )
    test = write_predictions(
        private / "peft_v4_condition_c_test_final.csv",
        predictions / "corrected_peft_test_predictions.csv",
        1850,
    )

    six = read_csv(private / "corrected_peft_sensitivity_six_method_predictions.csv", 1850)
    required = {
        "row_id",
        "clause_text",
        "clause_type",
        "contract_title",
        "TF-IDF + Logistic Regression",
        "Zero-shot",
        "Original PEFT",
        "RAG",
        "Hybrid",
        "Corrected PEFT (post-hoc)",
    }
    if not required.issubset(six.columns):
        raise ValueError(f"six-method file: missing columns {sorted(required - set(six.columns))}")
    if not six["clause_text"].equals(test["clause_text"]):
        raise ValueError("Corrected PEFT and six-method test rows are not text-aligned")
    if not six["clause_type"].equals(test["clause_type"]):
        raise ValueError("Corrected PEFT and six-method test rows are not label-aligned")
    if not six["Corrected PEFT (post-hoc)"].equals(test["predicted_label"]):
        raise ValueError("Corrected PEFT predictions differ between frozen source files")

    titles = sorted(six["contract_title"].dropna().unique())
    if len(titles) != 57:
        raise ValueError(f"Expected 57 document-title groups, found {len(titles)}")
    group_ids = {title: f"group_{position:03d}" for position, title in enumerate(titles, 1)}
    method_columns = [
        "TF-IDF + Logistic Regression",
        "Zero-shot",
        "Original PEFT",
        "RAG",
        "Hybrid",
        "Corrected PEFT (post-hoc)",
    ]
    public_six = six[["row_id", "clause_type", *method_columns]].copy()
    public_six.insert(1, "group_id", six["contract_title"].map(group_ids))
    public_six.to_csv(predictions / "six_method_test_predictions.csv", index=False)

    test_metrics = json.loads(
        (private / "peft_v4_condition_c_test_metrics.json").read_text(encoding="utf-8")
    )
    test_metrics["public_artifact"] = "results/predictions/corrected_peft_test_predictions.csv"
    test_metrics["sensitive_fields_removed"] = ["clause_text", "raw_output"]
    (metadata / "corrected_peft_test_metrics.json").write_text(
        json.dumps(test_metrics, indent=2) + "\n",
        encoding="utf-8",
    )

    test_configuration = json.loads(
        (private / "peft_v4_condition_c_test_metadata.json").read_text(encoding="utf-8")
    )
    test_configuration.pop("adapter", None)
    test_configuration["parser_implementation_note"] = (
        "The parser accepts a canonical label when either the complete cleaned response or its "
        "cleaned first line matches that label; all other responses are Unknown."
    )
    test_configuration["public_artifact"] = (
        "results/predictions/corrected_peft_test_predictions.csv"
    )
    (metadata / "corrected_peft_test_configuration.json").write_text(
        json.dumps(test_configuration, indent=2) + "\n",
        encoding="utf-8",
    )

    diagnostic = json.loads(
        (private / "peft_v4_validation_diagnostic_metadata.json").read_text(encoding="utf-8")
    )
    diagnostic.pop("adapter", None)
    diagnostic["public_artifact"] = (
        "results/predictions/corrected_peft_validation_predictions.csv"
    )
    diagnostic["sensitive_fields_removed"] = ["clause_text", "raw_output"]
    (metadata / "corrected_peft_validation_metadata.json").write_text(
        json.dumps(diagnostic, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json.loads(
        (private / "corrected_peft_sensitivity_summary.json").read_text(encoding="utf-8")
    )
    summary.pop("outputs", None)
    summary["public_artifacts"] = {
        "row_level_predictions": "results/predictions/six_method_test_predictions.csv",
        "aggregate_tables": "results/tables",
    }
    summary["privacy_note"] = (
        "Clause text, raw generations, real contract titles, and local account paths were removed. "
        "Document-title groups were replaced with stable anonymous identifiers."
    )
    (metadata / "corrected_peft_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    if not validation["row_id"].is_unique or not test["row_id"].is_unique:
        raise ValueError("Corrected PEFT row identifiers must be unique")
    print(f"Public artifacts written to {output}")


if __name__ == "__main__":
    main()
