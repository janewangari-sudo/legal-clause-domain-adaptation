# Chapter 6 - Limitations and Future Work

## 6.1 Scope and external validity

The experiments used one English-language dataset, 20 clause types and one
generative model family, `mistralai/Mistral-7B-Instruct-v0.2`. The ranking may
differ for other legal domains, languages, taxonomies, longer passages or model
families. The results therefore describe the implemented systems on this task
rather than legal NLP generally.

## 6.2 Experimental design

Corrected PEFT was developed after inspection of the original test behaviour.
Validation selected the inference condition, followed by one frozen corrected
test run, but this did not make it a prespecified member of the original
comparison. It remains a post-hoc sensitivity analysis.

The corrected run changed full-sequence loss to answer-only loss, while the
diagnostic varied prompt format and BOS handling. Because every combination was
not trained, the improvement cannot be assigned to one intervention. The
Hybrid has a related limitation: its original adapter was never trained on
retrieval-augmented prompts.

## 6.3 Data and task definition

Grouping by document title reduced obvious leakage, but the field was not
verified as a unique contract identifier. The 57 test groups must therefore not
be interpreted as 57 confirmed source contracts. Reusable legal boilerplate
also persists across differently titled documents.

Exact-text conflicts show that some isolated clauses contain insufficient
information for the recorded distinction. These cases may reflect legitimate
context-dependent functions, annotation problems or both. The deterministic
ceiling discussed in Section 4.7 applies only to exact clause-only
classification and may be exceeded when wider document context is available.

## 6.4 Measurement and statistical inference

The strict parser rejects valid labels followed by explanations, additional
labels or truncation. A leading-label sensitivity analysis increased Zero-shot
and RAG Accuracy but did not change the other methods or the ranking. Strict
scores remain primary because the rule was fixed before this secondary
analysis.

Row-level McNemar tests assume independent clauses despite clustering within
document titles, so their p-values are descriptive. The paired cluster
bootstrap resampled the 57 title groups, although inference from this number of
imperfectly identified groups remains limited.

The TF-IDF baseline was refitted to recover aligned predictions. Its archived
test metrics were reproduced exactly, but small training and validation
differences prevent a claim of bit-for-bit reproduction of the earlier fit.

## 6.5 Reproducibility and computational evidence

The experiments saved notebooks, predictions, checkpoints, metrics and
metadata, and the public repository separates reusable source code from
exploratory notebooks:
https://github.com/janewangari-sudo/legal-clause-domain-adaptation. These
materials make the analytical path auditable. They do not, however, guarantee
exact regeneration: the successful Colab environments were not fully pinned at
the time of the original runs, and later versions of CUDA, PyTorch,
Transformers or other libraries may behave differently. The modular `src/`
package was extracted after the principal experiments and should be understood
as a reproducibility refactor rather than the historical execution path for
every archived prediction.

Training time was recorded for the corrected adapter, which completed one
epoch in 2 hours 16 minutes 44 seconds in its reported session. Equivalent
wall-clock time, memory use, energy consumption and monetary cost were not
measured under a common protocol for all methods. The study can therefore make
qualitative observations about computational requirements, but not a reliable
cost-efficiency ranking.

## 6.6 Future work

An independently specified replication should freeze Corrected PEFT before
test inspection and cross full-sequence versus answer-only loss with matched
versus mismatched prompts. A retrieval-aware adapter should be trained on the
demonstration format used at inference. These experiments would separate
effects that changed together here.

Further work should review conflicting records against their source contracts
and test headings, neighbouring clauses and document metadata. Evaluation
should extend to additional datasets, languages and model families. Comparable
runtime, memory, energy and financial measurements are also required before
claiming cost efficiency. The present study does not establish generalisation
to unseen clause types or out-of-domain contracts.
