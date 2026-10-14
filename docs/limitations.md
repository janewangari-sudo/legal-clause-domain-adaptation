# Chapter 6 - Limitations and Future Work

## 6.1 Scope and external validity

The experiments were conducted on one English-language legal dataset and a fixed subset of 20 clause types. This design supported a controlled comparison, but it limits the reach of the findings. The observed ranking may not hold for other areas of law, document collections, languages, label definitions, or longer passages. In particular, the results should not be treated as evidence that one approach is generally superior for legal natural-language processing. They describe performance on the classification task and data split used in this study.

The generative methods also shared one base model, Mistral-7B-Instruct-v0.2. This kept the comparison between prompting, retrieval and adaptation more focused, while leaving model-family and scale effects untested. A different instruction-tuned model could respond differently to the prompts, retrieved examples, or adapter training. The study therefore compares adaptation strategies around a common model rather than the wider population of available large language models.

## 6.2 Experimental design

The corrected PEFT experiment is the most important design limitation. It was developed after the original PEFT results and their class-level errors had been examined. The three inference conditions were then compared on validation data, and the selected condition was evaluated once on the frozen test set. This procedure reduced further test-set selection, but it did not turn the corrected experiment into a prespecified member of the original five-method comparison. For this reason, the thesis reports the original comparison unchanged and presents Corrected PEFT as a post-hoc sensitivity analysis.

The corrected run changed the supervised target from full-sequence loss to answer-only loss. Its validation diagnostic separately examined the inference prompt and start-token handling, but the study did not train every combination of loss target and prompt format. It is therefore not possible to assign the observed improvement to a single change. The result supports the broader claim that implementation alignment mattered, not a causal estimate of the benefit of loss masking alone.

The Hybrid method has a related constraint. It reused the original adapter, which was not trained on prompts containing retrieved demonstrations. Its score shows what happened when retrieval was added at inference to that adapter; it does not establish the performance of an adapter trained specifically for retrieval-augmented inputs.

## 6.3 Data and task definition

Splitting by document title reduced obvious leakage between rows from the same titled document. However, the title field was not verified as a unique source-contract identifier. Generic titles may cause distinct contracts to be placed in the same group. This is conservative with respect to leakage, but it also means that the 57 test groups should not automatically be interpreted as 57 verified source agreements.

Repeated legal boilerplate created a more fundamental limitation. In the test partition, 245 rows contained one of 120 exact clause strings associated with more than one label. All methods performed much worse on these rows. Corrected PEFT, for example, achieved 0.4857 Accuracy on the conflict subset and 0.9570 on the remaining rows. The corresponding deterministic exact-text ceiling of 0.9330 is useful for diagnosing the clause-only task, but it is not a universal performance ceiling. A model given section headings, neighbouring clauses or document metadata could distinguish cases that are identical only after their context has been removed.

The conflicts cannot all be classified as annotation mistakes without manual review. The same date string may function as an Agreement Date in one contract and an Effective Date in another, and a transfer restriction may occur within a broader License Grant. Nevertheless, conflicting supervision means that an isolated-text classifier sometimes receives no evidence with which to recover the recorded label. This limits both training consistency and the interpretation of residual errors.

## 6.4 Measurement and statistical inference

The primary parser required the generated response to match one label exactly. This rule is reproducible and suitable for a closed-label task, but it counts a valid label followed by an explanation, a second label, or a truncated label as incorrect. A leading-label sensitivity check increased Zero-shot Accuracy by 0.0135 and RAG Accuracy by 0.0173; it did not change the other methods. The strict results remain primary because the parsing rule was fixed for the main analysis and relaxing it after observing outputs would add analytical discretion.

Row-level McNemar tests treat clauses as independent observations even though clauses are grouped within document titles. Their p-values are therefore reported only as descriptive paired checks. The main uncertainty analysis used a paired cluster bootstrap that resampled the 57 title groups. This better reflects within-group dependence, although a bootstrap based on 57 groups still has limited resolution and inherits any weakness in the grouping variable.

The TF-IDF baseline was refitted to recover aligned row-level predictions for the extended analysis. Its archived test metrics were reproduced exactly, but small numerical differences remained on the training and validation partitions. This does not change the reported test comparison, though it prevents a claim of bit-for-bit reproduction of the earlier fit.

## 6.5 Reproducibility and computational evidence

The experiments saved notebooks, predictions, checkpoints, metrics and metadata, and the repository now separates reusable source code from exploratory notebooks. These materials make the analytical path auditable. They do not, however, guarantee exact regeneration: the successful Colab environments were not fully pinned at the time of the original runs, and later versions of CUDA, PyTorch, Transformers or other libraries may behave differently. The modular `src/` package was also extracted after the principal experiments and should be understood as a reproducibility refactor rather than the historical execution path for every archived prediction.

Training time was recorded for the corrected adapter, which completed one epoch in 2 hours 16 minutes 44 seconds in its reported session. Equivalent wall-clock time, memory use, energy consumption and monetary cost were not measured under a common protocol for all methods. The study can therefore make qualitative observations about computational requirements, but not a reliable cost-efficiency ranking.

## 6.6 Future work

The strongest next step would be an independently specified replication in which the corrected PEFT configuration is fixed before any test results are seen. A complete factorial experiment could cross full-sequence and answer-only loss with matched and mismatched prompt formats. That design would separate effects that the present sensitivity study changed together. A retrieval-aware adapter should also be trained directly on prompts containing demonstrations before drawing a conclusion about the upper limit of a Hybrid approach.

Data-focused work is equally important. Conflicting examples should be reviewed against their source contracts, and models should be tested with section headings, neighbouring clauses and document metadata. Evaluation on additional legal datasets, languages and model families would show whether the findings generalise beyond this setting. Finally, future experiments should record training and inference time, peak memory, energy use and financial cost under a shared measurement protocol. These extensions would make it possible to judge not only which method is more accurate, but also which is reliable and practical for a particular legal classification workflow.
