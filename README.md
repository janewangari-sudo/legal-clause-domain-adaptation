# Legal Clause Domain Adaptation

Research software and reproducibility materials for the MSc thesis:

> **Comparative Analysis of Prompt Engineering, Parameter-Efficient Fine-Tuning,
> and Retrieval-Augmented Generation for Legal Domain Adaptation: An Empirical
> Study on Contract Clause Classification**

The study compares a TF-IDF logistic-regression baseline with four
Mistral-7B-Instruct approaches: zero-shot prompting, PEFT (LoRA), RAG, and a
PEFT–RAG hybrid on a frozen 20-class subset of CUAD.

## Main result

| Method | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| TF-IDF + Logistic Regression | **0.8605** | **0.8131** | **0.8559** |
| Hybrid | 0.8259 | 0.7764 | 0.8172 |
| RAG | 0.8157 | 0.7762 | 0.8315 |
| Zero-shot | 0.6227 | 0.6572 | 0.6615 |
| PEFT | 0.6146 | 0.6260 | 0.6199 |

Retrieval produced the largest improvement among the evaluated LLM adaptation
strategies. The Hybrid method achieved slightly higher accuracy than RAG, but
their overall Macro F1 values were effectively identical. The classical
baseline remained strongest on this fixed-label task.

## Repository status

The notebooks preserve the executed primary study and its stored outputs. The
modular package in `src/` is a subsequent, result-preserving refactor intended
to make validation and reuse easier. It must not be represented as the exact
code path that originally generated every archived output.

The corrected answer-only PEFT sensitivity study remains unfinished and does
not replace the frozen primary PEFT result.

## Repository structure

```text
configs/       Frozen labels and experiment settings
docs/          Methodology, data contract, limitations, and reproduction notes
notebooks/     Executed data-preparation and experiment records
results/       Machine-readable primary metrics and confidence intervals
scripts/       Small command-line entry points
src/           Reusable validation, baseline, prompting, and evaluation code
tests/         Methodological and integrity tests
```

## Split definition

The dataset contains 8,257 training, 833 validation, and 1,850 test clauses.
Splitting used the annotated document title derived from CUAD's
`Document Name-Answer` field. Clauses sharing the same title were kept in one
partition. The 193/35/57 group counts therefore describe document-title groups,
not verified unique source contracts.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
python scripts/validate_repository.py
```

To reproduce the classical baseline after placing the frozen split files in a
local data directory:

```bash
python scripts/run_baseline.py \
  --train data/processed/train.csv \
  --validation data/processed/val.csv \
  --test data/processed/test.csv \
  --output-dir artifacts/baseline
```

GPU experiments require the model, adapter, and retrieval artifacts documented
in the notebooks. They are deliberately not downloaded by the test suite or
GitHub Actions.

## Data and model availability

Raw CUAD data, model weights, adapters, caches, credentials, and large generated
artifacts are excluded from version control. Obtain CUAD from its official
source and review its licence before redistribution. Never commit Hugging Face,
Google Drive, Colab, or GitHub credentials.

## Reproducibility boundaries

- Random seed: `42`
- Frozen label count: `20`
- Primary metric: Macro F1
- Retrieval model: `sentence-transformers/all-MiniLM-L6-v2`
- Base LLM: `mistralai/Mistral-7B-Instruct-v0.2`
- Retrieval examples per query: `3`
- Unknown or non-canonical generated labels are scored as incorrect

See [`docs/reproduction.md`](docs/reproduction.md) for execution order and
[`docs/limitations.md`](docs/limitations.md) for unresolved constraints.

## Licence and citation

No software licence has been assigned yet. The repository is private while
redistribution rights, final author metadata, and thesis citation details are
being confirmed.
