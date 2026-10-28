# Results

These tables expose the authoritative headline results independently of the
notebook interface.

## Row-level predictions

- `predictions/corrected_peft_validation_predictions.csv` contains the 833
  validation rows for selected Condition C.
- `predictions/corrected_peft_test_predictions.csv` contains the 1,850 frozen
  Corrected PEFT test predictions.
- `predictions/six_method_test_predictions.csv` aligns all six reported methods
  on the same 1,850 test rows and replaces document titles with 57 anonymous
  group identifiers.

These files retain only row identifiers, true labels, predicted labels, and
anonymous group identifiers. Clause text, raw generations, real contract
titles, and local account paths were removed before publication. Label strings
retain their original experimental capitalization so the metrics can be
recomputed exactly.

Run the independent audit with:

```bash
python scripts/verify_frozen_results.py
```

The script checks row completeness and alignment, the frozen label schema,
anonymous group counts, unknown-output counts, and all reported Accuracy and
Macro F1 values. It does not require CUAD, a model download, or a GPU.

## Aggregate tables and metadata

- `tables/primary_metrics.csv` contains test metrics reported to four decimals.
- `tables/confidence_intervals.csv` contains percentile bootstrap intervals
  reported to four decimals.
- `tables/central_comparisons.csv` contains the four baseline comparisons shown
  in the notebook's final analysis. Values retain the notebook's displayed
  precision. An adjusted p-value displayed as `0.000000` is represented as
  `<0.0000005`; it must not be interpreted as an exact zero.
- `tables/peft_v4_validation_conditions.csv` records the validation-only prompt
  diagnostic used to select frozen Condition C.
- `tables/corrected_peft_sensitivity_metrics.csv` records the full-precision
  corrected PEFT test metrics.
- `tables/six_method_cluster_bootstrap.csv` contains the 57-group cluster
  intervals for the original methods and corrected PEFT sensitivity.
- `tables/corrected_peft_cluster_differences.csv` contains paired cluster
  bootstrap differences between corrected PEFT and each original method.
- `metadata/experiment_manifest.json` records the primary-study contract.
- `metadata/corrected_peft_validation_metadata.json` records the validation-only
  selection rule and confirms that the test set was not loaded.
- `metadata/corrected_peft_test_metrics.json` stores the full-precision frozen
  test metrics.
- `metadata/corrected_peft_test_configuration.json` records the selected prompt,
  BOS-token handling, generation settings, parser rule, and test freeze.
- `metadata/corrected_peft_summary.json` stores the privacy-safe final analysis
  summary without Google Drive paths.

The private project archive remains the authoritative record for full notebook
outputs, clause text, and raw generations. Those sensitive artifacts are not
duplicated here. The public files are sufficient to recompute the reported
classification metrics and audit test-row alignment. The original five-method
tables and the post-hoc sensitivity tables remain deliberately separate.
