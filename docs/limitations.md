# Limitations

- One base LLM and one legal classification dataset were evaluated.
- The original PEFT configuration received limited hyperparameter exploration.
- The answer-only PEFT sensitivity study is unfinished.
- The grouping variable is an annotated document title, not a verified unique
  source-contract identifier; distinct contracts with the same generic title
  may have been conservatively grouped together.
- Exact and near-exact legal boilerplate appears across partitions. These cases
  were audited and reported rather than automatically deleted.
- The baseline was re-fitted to recover row-level predictions. Archived test
  metrics reproduced exactly, while small training and validation numerical
  drift remained.
- The original successful Colab environment was not fully pinned.
- The modular `src/` package was extracted after the primary experiments and
  should be treated as a reproducibility refactor, not historical execution
  evidence.
