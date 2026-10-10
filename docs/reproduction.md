# Reproduction guide

## What can be reproduced locally

The validation suite, metric calculations, grouped-split checks, and classical
baseline can run on CPU. The Mistral experiments require substantially more
memory and the archived model, adapter, prediction, and retrieval artifacts.

## Execution order

1. Obtain CUAD v1 from the official source.
2. Review and configure paths in `notebooks/01_data_preparation.ipynb`.
3. Run data preparation to create the frozen CSV, PEFT, and RAG artifacts.
4. Run `notebooks/02_experiments.ipynb` for the primary five-method study.
5. Run `notebooks/03_peft_answer_only_control.ipynb` through
   `notebooks/05_peft_v4_condition_c_final_test.ipynb` in order for the
   post-hoc corrected PEFT sensitivity analysis. Do not rerun test selection or
   modify the frozen Condition C settings.
6. Run `notebooks/06_corrected_peft_final_statistics.ipynb` on CPU to reproduce
   the six-method descriptive tables, parser audit and 57-group cluster
   bootstrap.
7. Run repository validation and compare generated metrics with `results/`.

## Local validation

```bash
python -m pip install -e ".[dev]"
pytest
python scripts/validate_repository.py
```

## Baseline reproduction

```bash
python scripts/run_baseline.py \
  --train data/processed/train.csv \
  --validation data/processed/val.csv \
  --test data/processed/test.csv \
  --output-dir artifacts/baseline
```

The baseline implementation matches the archived vectorizer and classifier
settings. Exact reproduction still depends on compatible library versions.

## Environment caveat

The completed Colab run did not preserve a fully pinned environment. Do not
invent package versions. A lock file should be generated only from a verified
successful runtime; the current `pyproject.toml` defines supported ranges for
the CPU validation layer, not an exact reconstruction of the historical GPU
environment.
