# Literature-source and factual audit

## Purpose and status

This record documents the source and numerical checks completed on 14 October
2026. It is an audit aid rather than a thesis chapter. The frozen prediction
files and statistical tables remain the authority for experimental results;
the prose chapters must not be used to reconstruct those values.

The bibliography uses a consistent author-date format. Titles, author lists,
years, venues, pages and identifiers were checked against publisher,
conference or bibliographic records where available. All works cited in the
thesis chapters appear in `docs/bibliography.md`, and every bibliography entry
is cited in at least one chapter.

## Literature claim checks

| Thesis claim | Primary record checked | Audit outcome |
|---|---|---|
| LEGAL-BERT compared direct use, continued legal-domain pretraining and legal pretraining from scratch | ACL Anthology record and paper for Chalkidis et al. (2020) | Supported; metadata and DOI verified |
| LexGLUE found consistent benefits from legal-oriented models across its benchmark tasks | ACL Anthology record and paper for Chalkidis et al. (2022) | Supported; metadata and DOI verified |
| LegalBench contains 162 tasks covering six forms of legal reasoning and was developed with legal-professional input | NeurIPS proceedings record for Guha et al. (2023) | Supported; title, venue, pages and DOI verified |
| LEDGAR contains almost 100,000 provisions from more than 60,000 contracts | ACL Anthology record and paper for Tuggener et al. (2020) | Supported; title, authors, venue and pages verified; no DOI was assigned in the ACL record |
| CUAD contains 510 contracts, 13,101 labelled clauses and 41 label categories | NeurIPS Datasets and Benchmarks paper for Hendrycks et al. (2021) | Supported; the thesis uses “more than 13,000” where exact precision is unnecessary |
| Large autoregressive models can perform tasks from instructions and in-context examples without gradient updates | NeurIPS proceedings record for Brown et al. (2020) | Supported |
| Instruction tuning improves zero-shot task transfer | OpenReview record for Wei et al. (2022) | Supported |
| Legal prompting strategies do not transfer uniformly across models and long professional documents | ACL Anthology record and paper for Hakimi Parizi et al. (2023) | Supported; claim is phrased cautiously |
| General-purpose LLMs underperformed smaller legal fine-tuned models on the evaluated LEDGAR/LexGLUE setting | ACL Anthology record and paper for Jayakumar et al. (2023) | Supported for the reported experimental setting; not generalised beyond it |
| LoRA learns low-rank updates while the pretrained weights remain frozen | OpenReview record for Hu et al. (2022) | Supported |
| QLoRA uses a frozen four-bit model with LoRA and introduces NF4, double quantisation and paged optimisers | NeurIPS proceedings record for Dettmers et al. (2023) | Supported |
| Sentence-BERT produces sentence embeddings suitable for semantic similarity search | ACL Anthology record and paper for Reimers and Gurevych (2019) | Supported; metadata and DOI verified |
| The original RAG architecture combines retrieval with a sequence generator | NeurIPS proceedings record for Lewis et al. (2020) | Supported; the thesis explicitly distinguishes its in-context retrieval pipeline from that architecture |
| FAISS provides scalable dense-vector similarity search | IEEE record for Johnson, Douze and Jégou | Supported; DOI verified. The work was published online in 2019 and later appeared in volume 7(3), 2021, so the bibliography consistently uses the 2019 online-publication year |
| TF-IDF term weighting is grounded in classic information-retrieval work | Publisher record for Salton and Buckley (1988) | Supported; volume, pages and DOI verified |
| The bootstrap, McNemar test and Holm procedure support the stated statistical methods | Book/journal records for Efron and Tibshirani (1993), McNemar (1947) and Holm (1979) | Supported; McNemar DOI and Holm bibliographic record verified |

The review deliberately avoids unsupported claims that one adaptation method
is universally superior. Claims from comparative studies are limited to the
tasks and models those studies actually evaluated.

## Citation coverage

The following author-year keys are used across Chapters 2 and 3 and are all
present in the bibliography:

`Brown 2020`; `Chalkidis 2020`; `Chalkidis 2022`; `Dettmers 2023`;
`Efron and Tibshirani 1993`; `Guha 2023`; `Hakimi Parizi 2023`;
`Hendrycks 2021`; `Holm 1979`; `Hu 2022`; `Jayakumar 2023`; `Jiang 2023`;
`Johnson 2019`; `Lewis 2020`; `Liu 2023`; `McNemar 1947`; `Pedregosa 2011`;
`Reimers and Gurevych 2019`; `Salton and Buckley 1988`; `Tuggener 2020`; and
`Wei 2022`.

Pedregosa et al. (2011), previously present but uncited, is now cited where the
scikit-learn baseline implementation is described. No uncited bibliography
entry remains.

## Frozen factual sources

| Claim family | Authoritative repository evidence | Verified value or rule |
|---|---|---|
| Dataset size and schema | `results/metadata/experiment_manifest.json`; notebook 01 | 10,940 rows; 20 frozen classes; seed 42 |
| Partition sizes | Manifest; notebook 01 | 8,257 train; 833 validation; 1,850 test |
| Grouped split | Notebook 01; notebook 06 assertions | 193/35/57 document-title groups; 285 total; 20% of groups to test, then 15% of the remainder to validation |
| CUAD source transformation | Notebook 01 | 40 columns ending in `-Answer` identified the clause types; list-valued spans in the corresponding clause columns were expanded, yielding 12,984 rows before 20-class filtering. This is distinct from CUAD's 41 published categories |
| Primary test metrics | `results/tables/primary_metrics.csv` | All five original method values in Chapter 4 match the frozen table |
| Corrected PEFT metrics | `results/tables/corrected_peft_sensitivity_metrics.csv`; notebook 05 | Accuracy 0.8945945946; Macro F1 0.8459891224; Weighted F1 0.8860904227; no unknowns |
| Cluster intervals | `results/tables/six_method_cluster_bootstrap.csv` | 5,000 resamples over 57 groups; all Chapter 4 intervals match after four-decimal rounding |
| Paired differences | `results/tables/corrected_peft_cluster_differences.csv` | Corrected PEFT minus baseline: 0.034054 Accuracy and 0.032923 Macro F1; reported intervals match |
| LoRA and quantisation | Notebooks 02 and 03; adapter metadata | Rank 16; `lora_alpha=32`; dropout 0.05; q/k/v/o projections; NF4; double quantisation; 13,631,488 of 7,255,363,584 parameters trainable (0.1879%) |
| Original PEFT training | Notebook 02 | One epoch; learning rate 0.0002; effective batch 16; 2,048-token training sequences; full-sequence loss; training prompt omitted the label list |
| Corrected PEFT training | Notebook 03 | Answer-only loss; prompt tokens masked with `-100`; `add_special_tokens=False`; 517 steps; 2:16:44; validation loss 0.041306 |
| Validation prompt selection | Notebook 04 | A: 0.8595/0.7852; B: 0.8619/0.7922; C: 0.9256/0.8550 for Accuracy/Macro F1; C selected on validation |
| Generator input/output limits | Notebooks 02, 04 and 05 | 4,096-token inference input limit and 12 new-token generation limit for the reported generative evaluations |
| RAG and Hybrid truncation | Notebook 02 | Retrieved clauses 550 tokens each; query 1,500 tokens with a 75% beginning/25% ending rule; assembled prompt left-truncated to 4,096 tokens; three neighbours |
| Retrieval implementation | Notebook 02 | `all-MiniLM-L6-v2`; 384-dimensional unnormalised embeddings; FAISS `IndexFlatL2`; training partition only; top-three retrieval |
| Strict parser | Notebooks 02 and 04 | Case, surrounding quote/Markdown marks, optional `Category:` prefix and terminal punctuation are normalised; explanations, multiple labels, synonyms and truncated labels become `Unknown` |
| Exact-text conflicts | Executed notebook 06 and its exported Drive artifacts | 120 conflicting unique texts; 245 test rows (13.24%); deterministic exact-text ceiling 0.9330 |
| Corrected PEFT conflict subsets | Executed notebook 06 | Accuracy 0.4857 on 245 conflict rows and 0.9570 on 1,605 non-conflict rows; Macro F1 0.4186 and 0.9162 respectively |
| Corrected PEFT class results | Executed notebooks 05 and 06 | Chapter 4 precision, recall, F1 and support values match all 20 frozen rows |
| Parser sensitivity | Executed notebook 06 | Leading-label parsing changes Accuracy by +0.0135 for Zero-shot and +0.0173 for RAG; primary strict scores remain unchanged |

## Audit decisions and boundaries

- Values in the chapters are rounded from frozen machine-readable tables, not
  copied from intermediate notebook progress displays.
- Corrected PEFT remains labelled post-hoc and validation-selected. Its test
  result does not replace or retroactively redesign the original five-method
  comparison.
- The 57 test groups are annotated document-title groups, not 57 verified
  unique contracts.
- The 0.9330 exact-text figure is a deterministic clause-string ceiling, not a
  universal task ceiling.
- The raw data and row-level prediction files are intentionally excluded from
  GitHub. Claims that require them are also backed by the executed notebook
  assertions and exported aggregate tables retained in the repository.
- Package versions or cost figures absent from saved evidence are not inferred
  from memory. The manuscript states these reproducibility limits explicitly.
