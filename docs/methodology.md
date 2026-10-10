# Chapter 3 — Methodology

## 3.1 Research design and analysis status

This study compared five approaches to classifying contract clauses into a
fixed set of 20 legal categories: TF-IDF with logistic regression, zero-shot
prompting, parameter-efficient fine-tuning (PEFT), retrieval-augmented
generation (RAG), and a PEFT–RAG hybrid. The same frozen training, validation,
and test partitions were used throughout. Macro F1 was the main performance
measure because the class distribution was imbalanced and equal attention to
each category was required.

The analysis had two stages. The first stage was the original five-method
comparison. Its predictions and results were frozen before the second stage.
Inspection of the original PEFT errors then revealed a methodological concern:
the adapter had been trained and evaluated with different prompt wording, and
the training loss had been calculated over the complete prompt-and-answer
sequence. A controlled, post-hoc sensitivity study was therefore conducted to
test an answer-only loss and to diagnose the inference-prompt mismatch.

This second stage was not fixed before the original test results were seen. The
variants in the sensitivity study were selected using the validation set only.
Once the validation rule selected a configuration, that configuration was
evaluated once on the test set. The original five-method results remain in the
record; the corrected PEFT result is reported separately as a post-hoc,
validation-selected sensitivity analysis. This distinction prevents a
methodological correction from being presented as if it had been part of the
original comparison.

## 3.2 Dataset and classification task

The data were derived from version 1 of the Contract Understanding Atticus
Dataset (CUAD), an expert-annotated resource for legal contract review
(Hendrycks et al., 2021). The study used a frozen subset containing 10,940
clause instances across 20 clause types. Each observation contained the clause
text, its clause-type label, and an annotated document-title value stored in the
project as `contract_title`.

Empty clause entries were removed, surrounding whitespace was stripped, and
the original letter case was retained. The label set was fixed before the
experiments. No labels were added, merged, or removed after model evaluation.

## 3.3 Grouped data partitioning

The clauses were partitioned using a two-stage grouped split with random seed
42. All rows sharing the same annotated document-title value were assigned to
one partition. First, 20% of the 285 document-title groups were assigned to the
test set. Of the remaining groups, 15% were assigned to validation and the rest
to training. The resulting partitions were:

| Partition | Clauses | Document-title groups |
|---|---:|---:|
| Training | 8,257 | 193 |
| Validation | 833 | 35 |
| Test | 1,850 | 57 |
| **Total** | **10,940** | **285** |

There was no document-title-group overlap between the partitions. The grouping
field should not, however, be described as a verified contract identifier.
Different contracts can share a generic annotated title, and repeated legal
boilerplate can occur across different groups.

## 3.4 Compared methods

### 3.4.1 TF-IDF and logistic-regression baseline

The classical baseline represented each clause with TF-IDF-weighted unigrams
and bigrams. The vocabulary was limited to 5,000 features. A logistic-regression
classifier used balanced class weights, a maximum of 1,000 iterations, and
random seed 42. This method generated one of the 20 labels directly and could
not produce an unknown textual response.

### 3.4.2 Zero-shot prompting

The zero-shot method used `mistralai/Mistral-7B-Instruct-v0.2` without updating
its parameters. Mistral 7B is an instruction-capable seven-billion-parameter
model that uses grouped-query and sliding-window attention (Jiang et al., 2023).
Each clause was supplied with the complete class list and an instruction to
return only one category name. Decoding was deterministic.

### 3.4.3 Original PEFT

The original PEFT method adapted the same Mistral model with Low-Rank
Adaptation. LoRA freezes the pretrained weights and learns low-rank update
matrices, reducing the number of trainable parameters (Hu et al., 2021). The
base model was loaded in four-bit NF4 form with double quantisation, following
the memory-saving principles of QLoRA (Dettmers et al., 2023).

The adapter used rank 16, scaling factor 32, dropout 0.05, and the `q_proj`,
`k_proj`, `v_proj`, and `o_proj` target modules. Training used one epoch, a
learning rate of 0.0002, effective batch size 16, seed 42, and 2,048-token
training sequences. There were 13,631,488 trainable parameters, representing
approximately 0.1879% of the 7,255,363,584 total parameters.

In the original run, loss was calculated across the full formatted sequence.
In addition, the training prompt and the label-list inference prompt were not
identical. These differences were discovered after the original test error
analysis and motivated the sensitivity study described in Section 3.5.

### 3.4.4 Retrieval-augmented generation

The RAG method embedded the training clauses with
`sentence-transformers/all-MiniLM-L6-v2`. Sentence-transformer models produce
fixed-size semantic representations suitable for similarity search (Reimers &
Gurevych, 2019). The unnormalised vectors were stored in a FAISS `IndexFlatL2`
index (Johnson et al., 2017). For each query, the three nearest training
examples were inserted into the classification prompt. This implementation
used retrieval as in-context evidence rather than jointly training the
retriever and generator; it is therefore a task-specific RAG pipeline rather
than the end-to-end architecture introduced by Lewis et al. (2020).

### 3.4.5 PEFT–RAG hybrid

The hybrid method combined the original LoRA adapter with the three retrieved
examples used by RAG. No additional training was performed. Because the
original adapter had not been trained on retrieval-style prompts, the hybrid
tested whether retrieved demonstrations helped at inference time; it did not
test a retrieval-aware fine-tuning objective.

## 3.5 Corrected PEFT sensitivity study

### 3.5.1 Controlled answer-only training

The sensitivity adapter retained the original data, prompt construction, base
model, LoRA configuration, learning rate, effective batch size, seed, and
one-epoch schedule. Its training objective differed in one substantive way:
instruction and clause tokens were assigned the ignore index `-100`, so only
the category answer and end-of-sequence token contributed to the causal
language-model loss. Prompts were tokenised with
`add_special_tokens=False` because the chat template already supplied a
beginning-of-sequence token.

Training completed 517 optimisation steps in 2 hours, 16 minutes and 44
seconds. The final checkpoint had validation loss 0.041306. The training and
validation partitions contained 8,257 and 833 rows respectively; the test set
was not loaded during this run.

### 3.5.2 Validation-only prompt diagnostic

The completed adapter was evaluated under three validation conditions:

| Condition | Prompt and tokenisation |
|---|---|
| A | Label-list inference prompt with the original default tokenisation |
| B | The same label-list prompt with `add_special_tokens=False`, giving one BOS token |
| C | The exact v4 training prompt with `add_special_tokens=False`, giving one BOS token |

The selection metric was validation Macro F1, with accuracy used only as a
secondary ordering measure. A change of at least 0.01 Macro F1, or a major
class-level recovery or collapse, was treated as material. Condition C achieved
the highest validation Macro F1 and was frozen before test evaluation. No
retraining occurred during this diagnostic.

Condition C used the instruction “Classify the following contract clause into
its correct clause type”, followed by the clause and the output-format
instruction. Unlike the label-list prompt, it did not include the 20 class names
in the inference prompt. This matched the prompt seen during v4 training.

### 3.5.3 Frozen corrected test evaluation

Condition C was evaluated once on all 1,850 test rows. The base model, adapter,
prompt, tokenisation, deterministic decoding, 12-token generation limit, and
strict parser were frozen beforehand. Alternative prompt conditions were not
evaluated on the test set, and no further model selection was permitted after
the corrected test predictions were inspected.

## 3.6 Output parsing and failure handling

Generated responses were assessed with a strict parser. It accepted a class
name only when the complete cleaned response matched one frozen label, with
limited tolerance for case, surrounding quotation or Markdown characters, an
optional `Category:` prefix, and terminal punctuation. Explanations, multiple
labels, truncated labels, synonyms, and other non-canonical outputs were mapped
to `Unknown` and scored as incorrect.

A secondary parser analysis accepted a valid label at the start of a generated
response followed by additional text. This analysis quantified formatting
sensitivity but did not replace the strict primary scores.

## 3.7 Evaluation and statistical analysis

Macro F1 was the primary metric. Accuracy, Macro Precision, Macro Recall,
Weighted F1, unknown-output rate, per-class precision, recall and F1 were also
reported. Macro metrics were calculated across the fixed 20-class schema with
zero contribution from classes whose denominator was zero.

Clauses from the same document-title group cannot safely be treated as
independent observations. The main uncertainty analysis therefore used 5,000
paired cluster-bootstrap resamples over the 57 test document-title groups. For
each resample, 57 groups were drawn with replacement, all clauses belonging to
each sampled group were included, and the same sampled groups were used for
every method. Percentile 95% intervals were calculated for Accuracy, Macro F1,
and pairwise method differences. A pairwise interval excluding zero was treated
as evidence that the observed difference was robust to document-title-group
resampling.

Exact McNemar tests with Holm correction were retained as descriptive paired
row-level checks. Their p-values were not treated as the main inferential
evidence because the independence assumption is questionable for clauses
nested within 57 groups.

## 3.8 Exact-text conflict analysis

An additional audit identified clause strings that appeared with more than one
true label within a partition. Performance was calculated separately for rows
with and without such conflicts. A deterministic exact-text ceiling was
calculated by assigning each unique clause string its most frequent label and
summing the resulting correct assignments. This is a ceiling for deterministic
classification based only on the exact clause string; it is not a universal
ceiling for systems that use wider document context.

## 3.9 Reproducibility and experiment preservation

All splits, labels and random seeds were frozen. Prediction files were audited
for row identifiers, clause text, true labels, duplicates, and schema-invalid
predictions before comparison. Interrupted GPU tasks wrote partial outputs and
resumed from saved checkpoints. The original five-method artifacts and the
corrected PEFT artifacts were saved under different filenames so the historical
record could not be silently overwritten.

The experiments were run in Google Colab, principally on an NVIDIA T4 runtime.
The successful historical environment was not fully pinned; consequently, no
unverified package versions are claimed. The notebooks, saved predictions,
adapter metadata, statistical outputs, and repository validation checks form
the reproducibility record. The modular `src/` package was created after the
experiments and is identified as a refactor rather than the original execution
path.

## References cited in this chapter

- Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). QLoRA:
  Efficient finetuning of quantized LLMs. *Advances in Neural Information
  Processing Systems, 36*.
- Hendrycks, D., Burns, C., Chen, A., & Ball, S. (2021). CUAD: An
  expert-annotated NLP dataset for legal contract review. *Advances in Neural
  Information Processing Systems, 34*.
- Hu, E. J., et al. (2021). LoRA: Low-rank adaptation of large language models.
  *arXiv preprint arXiv:2106.09685*.
- Jiang, A. Q., et al. (2023). Mistral 7B. *arXiv preprint arXiv:2310.06825*.
- Johnson, J., Douze, M., & Jégou, H. (2017). Billion-scale similarity search
  with GPUs. *arXiv preprint arXiv:1702.08734*.
- Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive
  NLP tasks. *Advances in Neural Information Processing Systems, 33*.
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using
  Siamese BERT-networks. *Proceedings of EMNLP-IJCNLP*, 3982–3992.
