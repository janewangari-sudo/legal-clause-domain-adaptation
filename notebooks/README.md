# Notebooks

Run the notebooks in numerical order:

1. `01_data_preparation.ipynb`
2. `02_experiments.ipynb`

Post-hoc PEFT sensitivity and diagnostic notebooks:

3. `03_peft_answer_only_control.ipynb` — controlled answer-only training and
   validation evaluation; it deliberately stops before the test split.
4. `04_peft_v4_validation_diagnostics.ipynb` — reuses the completed v4 adapter
   to isolate BOS-token and inference-prompt differences on validation only. It
   does not train and does not load the test split.
5. `05_peft_v4_condition_c_final_test.ipynb` — performs the single frozen test
   evaluation of validation-selected Condition C: the completed answer-only v4
   adapter, its exact training prompt and one BOS token. It checkpoints test
   predictions and evaluates no alternative configuration.
6. `06_corrected_peft_final_statistics.ipynb` — performs the CPU-only final
   statistical analysis of the six frozen prediction sets. It preserves the
   original five-method comparison, treats corrected PEFT as a post-hoc
   sensitivity condition, adds document-title-group cluster-bootstrap
   intervals, and keeps row-level McNemar tests explicitly descriptive.

The first two notebooks preserve stored outputs from the completed primary
study. Notebooks 03–06 preserve the runnable code and frozen settings for the
corrected PEFT sensitivity workflow but are committed without execution output.
Privacy-safe row-level predictions and full-precision metric metadata are
published separately under `results/` and can be checked with
`scripts/verify_frozen_results.py`.

A later documentation-only commit corrected the split terminology from
“contract-level” to “document-title-group” without changing the data,
predictions, or scores.

The modular code under `src/` is a post-experiment refactor. Use the notebooks
as the historical execution record and the package for validation and reuse.
