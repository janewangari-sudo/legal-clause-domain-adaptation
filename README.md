# Legal Clause Domain Adaptation

Private research repository for an MSc thesis comparing prompt engineering,
parameter-efficient fine-tuning (PEFT), retrieval-augmented generation (RAG),
a PEFT–RAG hybrid, and a TF-IDF logistic-regression baseline for legal contract
clause classification.

## Repository status

The notebooks in `notebooks/` are the frozen, cleaned record of the completed
primary study. They are being preserved unchanged in the initial repository
snapshot. Methodological terminology corrections and further restructuring will
be made in later commits so that the project history remains transparent.

## Initial notebooks

- `01_data_preparation.ipynb` — CUAD extraction, cleaning, grouped splitting,
  leakage audits, baseline preparation, PEFT data export, and RAG index creation.
- `02_experiments.ipynb` — zero-shot, PEFT, RAG, hybrid, classical baseline,
  statistical comparison, per-class analysis, and figures.

## Primary results

| Method | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| TF-IDF + Logistic Regression | 0.8605 | 0.8131 | 0.8559 |
| Hybrid | 0.8259 | 0.7764 | 0.8172 |
| RAG | 0.8157 | 0.7762 | 0.8315 |
| Zero-shot | 0.6227 | 0.6572 | 0.6615 |
| PEFT | 0.6146 | 0.6260 | 0.6199 |

## Data and model files

Raw CUAD data, model weights, adapters, caches, credentials, and generated
large artifacts are intentionally excluded from version control. Reproduction
instructions, software versions, configuration files, scripts, figures, and
machine-readable result summaries will be added during repository cleanup.

## Current scope

The completed notebooks document the primary experiment. The proposed
answer-only PEFT sensitivity study is separate and unfinished; it does not
replace the frozen primary PEFT result.
