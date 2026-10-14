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
    "docs/source_and_factual_audit.md",
    "results/tables/primary_metrics.csv",
    "results/tables/confidence_intervals.csv",
    "results/metadata/experiment_manifest.json",
)

CITATION_KEYS = (
    ("Brown", 2020),
    ("Chalkidis", 2020),
    ("Chalkidis", 2022),
    ("Dettmers", 2023),
    ("Efron", 1993),
    ("Guha", 2023),
    ("Hakimi Parizi", 2023),
    ("Hendrycks", 2021),
    ("Holm", 1979),
    ("Hu", 2022),
    ("Jayakumar", 2023),
    ("Jiang", 2023),
    ("Johnson", 2019),
    ("Lewis", 2020),
    ("Liu", 2023),
    ("McNemar", 1947),
    ("Pedregosa", 2011),
    ("Reimers", 2019),
    ("Salton", 1988),
    ("Tuggener", 2020),
    ("Wei", 2022),
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


def validate_thesis_sources_and_facts() -> None:
    literature = (ROOT / "docs/literature_review.md").read_text(encoding="utf-8")
    methodology = (ROOT / "docs/methodology.md").read_text(encoding="utf-8")
    bibliography = (ROOT / "docs/bibliography.md").read_text(encoding="utf-8")
    results_chapter = (ROOT / "docs/results.md").read_text(encoding="utf-8")
    cited_text = literature + "\n" + methodology

    for author, year in CITATION_KEYS:
        if author not in cited_text or str(year) not in cited_text:
            raise ValueError(f"Expected in-text citation is missing: {author} {year}")
        if author not in bibliography or f"({year})" not in bibliography:
            raise ValueError(f"Bibliography entry is missing: {author} {year}")

    primary = pd.read_csv(ROOT / "results/tables/primary_metrics.csv")
    display_names = {"PEFT": "Original PEFT"}
    for row in primary.itertuples(index=False):
        method = display_names.get(row.method, row.method)
        matching_lines = [
            line.replace("**", "")
            for line in results_chapter.splitlines()
            if line.startswith(f"| {method} |")
        ]
        required_values = (
            f"{row.accuracy:.4f}",
            f"{row.macro_precision:.4f}",
            f"{row.macro_recall:.4f}",
            f"{row.macro_f1:.4f}",
            f"{row.weighted_f1:.4f}",
        )
        if not any(all(value in line for value in required_values) for line in matching_lines):
            raise ValueError(f"Chapter 4 primary-metric row is stale: {method}")

    cluster = pd.read_csv(ROOT / "results/tables/six_method_cluster_bootstrap.csv")
    for row in cluster.itertuples(index=False):
        method = row.method.replace(" (post-hoc)", "")
        expected = (
            f"| {method} | {row.accuracy:.4f} | "
            f"[{row.accuracy_ci_lower:.4f}, {row.accuracy_ci_upper:.4f}] | "
            f"{row.macro_f1:.4f} | "
            f"[{row.macro_f1_ci_lower:.4f}, {row.macro_f1_ci_upper:.4f}] |"
        )
        if expected not in results_chapter:
            raise ValueError(f"Chapter 4 cluster-bootstrap row is stale: {method}")

    required_methodology_facts = (
        "8,257 | 193",
        "833 | 35",
        "1,850 | 57",
        "13,631,488 trainable parameters",
        "0.1879%",
        "550",
        "1,500",
        "4,096",
        "12-token",
    )
    for fact in required_methodology_facts:
        if fact not in methodology:
            raise ValueError(f"Methodology fact is missing: {fact}")


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

    validate_thesis_sources_and_facts()

    print("Repository validation passed.")


if __name__ == "__main__":
    main()
