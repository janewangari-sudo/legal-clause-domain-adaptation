"""Run lightweight repository checks without downloading data or models."""

import json
from pathlib import Path

import pandas as pd

from legal_clause_adaptation import FROZEN_LABELS

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "configs/labels.yaml",
    "configs/primary_experiments.yaml",
    "notebooks/01_data_preparation.ipynb",
    "notebooks/02_experiments.ipynb",
    "results/tables/primary_metrics.csv",
    "results/tables/confidence_intervals.csv",
    "results/metadata/experiment_manifest.json",
)


def validate_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    if not cells:
        raise ValueError(f"Notebook has no cells: {path}")
    cell_ids = [cell.get("id") for cell in cells if cell.get("id")]
    if len(cell_ids) != len(set(cell_ids)):
        raise ValueError(f"Notebook contains duplicate cell IDs: {path}")
    if any(not "".join(cell.get("source", [])).strip() for cell in cells):
        raise ValueError(f"Notebook contains an empty cell: {path}")
    stored_errors = [
        cell for cell in cells for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    if stored_errors:
        raise ValueError(f"Notebook contains stored error outputs: {path}")


def main() -> None:
    missing = [relative for relative in REQUIRED_FILES if not (ROOT / relative).exists()]
    if missing:
        raise FileNotFoundError(f"Required repository files are missing: {missing}")

    for relative in REQUIRED_FILES:
        if relative.endswith(".ipynb"):
            validate_notebook(ROOT / relative)

    manifest = json.loads(
        (ROOT / "results/metadata/experiment_manifest.json").read_text(encoding="utf-8")
    )
    if manifest["dataset"]["classes"] != len(FROZEN_LABELS):
        raise ValueError("Manifest class count differs from the frozen label schema")
    if manifest["dataset"]["split_unit"] != "annotated_document_title_group":
        raise ValueError("Manifest reports the wrong split unit")

    metrics = pd.read_csv(ROOT / "results/tables/primary_metrics.csv")
    expected_methods = [
        "TF-IDF + Logistic Regression",
        "Zero-shot",
        "PEFT",
        "RAG",
        "Hybrid",
    ]
    if metrics["method"].tolist() != expected_methods:
        raise ValueError("Primary metrics method order or membership changed")
    if not metrics.loc[metrics["method"].eq("TF-IDF + Logistic Regression"), "macro_f1"].eq(
        0.8131
    ).all():
        raise ValueError("Archived baseline Macro F1 changed")

    print("Repository validation passed.")


if __name__ == "__main__":
    main()
