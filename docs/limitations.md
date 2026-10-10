# Limitations

- The study used one legal dataset, one 20-class subset, and one base language
  model. The findings therefore do not establish that the same ordering will
  hold for other legal tasks, languages, model families, or larger models.
- The corrected PEFT experiment was motivated after inspection of the original
  PEFT test behaviour. Its prompt condition was subsequently selected using
  validation data and evaluated once on test, but it remains post-hoc and must
  not be presented as part of the original fixed comparison.
- The corrected adapter changed the loss objective from full-sequence to
  answer-only supervision. The later validation diagnostic isolated the BOS
  and inference-prompt effects, but no complete 2 × 2 retraining design was
  performed. The separate causal contribution of every training choice cannot
  therefore be estimated.
- The hybrid reused an adapter that had not been trained on retrieval-style
  prompts. Its result does not show how retrieval-aware PEFT training would
  perform.
- The grouping variable is an annotated document title rather than a verified
  unique source-contract identifier. Distinct contracts with the same generic
  title may have been conservatively grouped together.
- Exact and near-exact legal boilerplate occurs across the data. In the test
  partition, 245 rows contained one of 120 exact clause strings associated with
  multiple labels. These ambiguities limit what a classifier using only clause
  text can resolve.
- The deterministic exact-text ceiling is not a universal performance ceiling.
  Models supplied with document-level context could potentially distinguish
  examples that have identical isolated clause text.
- Strict parsing counts explanations, multiple labels and truncated class names
  as incorrect. The leading-label sensitivity analysis shows that this choice
  modestly affects Zero-shot and RAG, although it does not affect Corrected
  PEFT, Hybrid, or Original PEFT in the final predictions.
- Row-level McNemar p-values do not account for clustering and are interpreted
  descriptively. The document-title-group cluster bootstrap is the main
  robustness analysis, but it is based on only 57 test groups.
- The baseline was re-fitted to recover row-level predictions. Archived test
  metrics reproduced exactly, while small training and validation numerical
  drift remained.
- The successful Colab environments were not fully pinned. Saved predictions,
  checkpoints, metadata and executed notebooks mitigate this limitation but do
  not guarantee bit-for-bit regeneration on a future software stack.
- Training time was recorded for the corrected adapter, but a complete,
  consistently measured comparison of energy use, latency and financial cost
  across all methods was not obtained.
- The modular `src/` package was extracted after the main experiments. It is a
  reproducibility refactor, not the historical code path that produced every
  archived prediction.
