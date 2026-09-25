# Results

These tables expose the authoritative headline results independently of the
notebook interface.

- `tables/primary_metrics.csv` contains test metrics reported to four decimals.
- `tables/confidence_intervals.csv` contains percentile bootstrap intervals
  reported to four decimals.
- `tables/central_comparisons.csv` contains the four baseline comparisons shown
  in the notebook's final analysis. Values retain the notebook's displayed
  precision. An adjusted p-value displayed as `0.000000` is represented as
  `<0.0000005`; it must not be interpreted as an exact zero.
- `metadata/experiment_manifest.json` records the primary-study contract.

The executed notebook and archived files in the original project directory
remain the authoritative source for full-precision statistics and row-level
predictions. Those large or sensitive artifacts are not duplicated here.
