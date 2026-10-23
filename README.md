# Legal Clause Domain Adaptation

Research software and reproducibility materials for the MSc thesis:

> **An Empirical Comparison of Prompting, Parameter-Efficient Fine-Tuning, and
> Retrieval-Augmented Generation for Legal Contract Clause Classification**

The study compares a TF-IDF logistic-regression baseline with four
Mistral-7B-Instruct approaches: zero-shot prompting, PEFT (LoRA), RAG, and a
PEFT–RAG hybrid on a frozen 20-class subset of CUAD.

## Results

### Original five-method comparison

| Method | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| TF-IDF + Logistic Regression | **0.8605** | **0.8131** | **0.8559** |
| Hybrid | 0.8259 | 0.7764 | 0.8172 |
| RAG | 0.8157 | 0.7762 | 0.8315 |
| Zero-shot | 0.6227 | 0.6572 | 0.6615 |
| PEFT | 0.6146 | 0.6260 | 0.6199 |

Retrieval produced the largest improvement among the LLM approaches in the
original comparison. The Hybrid method achieved slightly higher accuracy than
RAG, but their Macro F1 values were effectively identical. The classical
baseline was the strongest original method.

### Corrected PEFT sensitivity

A post-hoc PEFT sensitivity study corrected the training objective and matched
the inference prompt to the training prompt. The condition was selected on
validation and then evaluated once on test.

| Method | Analysis status | Accuracy | Macro F1 | Weighted F1 |
|---|---|---:|---:|---:|
| Corrected PEFT | Post-hoc sensitivity | **0.8946** | **0.8460** | **0.8861** |
| TF-IDF + Logistic Regression | Original comparison | 0.8605 | 0.8131 | 0.8559 |

The corrected PEFT advantage over the baseline was 0.0341 Accuracy (95%
document-title-group cluster-bootstrap CI [0.0230, 0.0460]) and 0.0329 Macro F1
(95% CI [0.0162, 0.0516]). This qualifies the original conclusion but does not
erase the original PEFT result or convert the sensitivity study into a
preplanned experiment.

## Repository status

The notebooks preserve the executed primary study and its stored outputs. The
modular package in `src/` is a subsequent, result-preserving refactor intended
to make validation and reuse easier. It must not be represented as the exact
code path that originally generated every archived output.

The corrected answer-only PEFT sensitivity study is complete. Its artifacts
are kept separate from the original five-method study and are explicitly
labelled post-hoc and validation-selected.

## Repository structure

```text
configs/       Frozen labels and experiment settings
docs/          Thesis chapter drafts, data contract, limitations, and reproduction notes
notebooks/     Executed data-preparation and experiment records
results/       Machine-readable primary metrics and confidence intervals
scripts/       Small command-line entry points
src/           Reusable validation, baseline, prompting, and evaluation code
tests/         Methodological and integrity tests
```

## Thesis manuscript

The seven thesis chapters are maintained as reviewable Markdown files under
`docs/`. The formatted Word draft is generated locally and is deliberately not
tracked because it contains submission-specific personal and administrative
fields.

```bash
python -m pip install -e ".[thesis]"
python scripts/build_thesis_document.py
```

Before generating a submission copy, confirm the exact approved title,
candidate details, programme wording, supervisor name and academic title. The
mandatory AI-use declaration is included at the end of the generated draft.

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

See [`docs/reproduction.md`](docs/reproduction.md) for execution order,
[`docs/source_and_factual_audit.md`](docs/source_and_factual_audit.md) for the
claim-to-evidence audit, and [`docs/limitations.md`](docs/limitations.md) for
unresolved constraints.

## Public repository and citation

This public repository contains the code, notebooks and aggregate outputs
needed to audit the thesis results. Raw CUAD data, model weights, adapters,
credentials and submission-specific thesis files are not included. No software
licence has yet been assigned, so public availability should not be interpreted
as permission to redistribute or modify the material beyond rights provided by
law. Final thesis citation details will be added after submission.
