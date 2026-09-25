"""Fit and evaluate the archived classical baseline on frozen CSV splits."""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd

from legal_clause_adaptation import EXPECTED_SPLIT_SIZES, FROZEN_LABELS
from legal_clause_adaptation.data import validate_split_collection
from legal_clause_adaptation.evaluation import classification_metrics
from legal_clause_adaptation.methods import fit_baseline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    splits = {
        "train": pd.read_csv(args.train),
        "validation": pd.read_csv(args.validation),
        "test": pd.read_csv(args.test),
    }
    validate_split_collection(
        splits,
        labels=FROZEN_LABELS,
        expected_sizes=EXPECTED_SPLIT_SIZES,
    )

    model = fit_baseline(splits["train"]["clause_text"], splits["train"]["clause_type"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metric_records = []
    for split_name in ("validation", "test"):
        frame = splits[split_name].copy()
        predictions = model.predict(frame["clause_text"])
        frame["predicted_label_baseline"] = predictions
        frame.to_csv(args.output_dir / f"{split_name}_predictions.csv", index=False)
        metric_records.append(
            {
                "split": split_name,
                **classification_metrics(
                    frame["clause_type"], predictions, labels=FROZEN_LABELS
                ),
            }
        )

    pd.DataFrame(metric_records).to_csv(args.output_dir / "metrics.csv", index=False)
    joblib.dump(model, args.output_dir / "baseline_pipeline.joblib")
    metadata = {
        "random_seed": 42,
        "vectorizer": {"max_features": 5000, "ngram_range": [1, 2]},
        "classifier": {"max_iter": 1000, "class_weight": "balanced"},
    }
    (args.output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
