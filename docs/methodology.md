# Chapter 3 - Methodology

## 3.1 Research design and analysis status

The empirical task was to assign a contract clause to one of 20 legal
categories. Five methods were compared on the same data partitions: TF-IDF
with logistic regression, zero-shot prompting, parameter-efficient
fine-tuning (PEFT), retrieval-augmented generation (RAG), and a PEFT-RAG
hybrid. Macro F1 was chosen as the primary measure because the class frequencies
were uneven. Unlike accuracy, it gives each category the same weight and
therefore makes poor performance on the smaller classes visible.

The work developed in two stages. The first was the planned five-method
comparison. Those predictions were saved before any corrective PEFT work was
undertaken. Examination of the original PEFT errors exposed two weaknesses in
that run. The training loss covered the instruction and clause as well as the
answer, and the inference prompt contained the full label list whereas the
training prompt did not. A controlled sensitivity study was then used to test
answer-only loss and to measure the effect of matching the inference prompt to
the prompt used in training.

The sensitivity study was designed after the original test behaviour had been
examined, so it cannot be treated as part of the original comparison. Its
inference conditions were compared on validation data only. The selected
condition was then run once on the test set. Accordingly, the thesis retains
the original five results and reports corrected PEFT separately as a post-hoc,
validation-selected analysis. This chronology matters: the corrected result
shows what happened after repairing the training and inference procedure, but
it is not an unbiased sixth member of the original design.

## 3.2 Dataset and classification task

The data were derived from version 1 of the Contract Understanding Atticus
Dataset (CUAD), an expert-annotated resource for legal contract review
(Hendrycks et al., 2021). CUAD contains 510 contracts and 41 published label
categories. In the project's `master_clauses.csv` representation, the
extraction code used the 40 columns whose names ended in `-Answer` to identify
the clause types, then expanded the list-valued spans in the corresponding
clause columns so that each extracted clause became one observation. This
produced 12,984 clauses before class filtering. The analysis used a fixed set
of 20 clause types, leaving 10,940 observations. Each
observation contained the clause text, its clause-type label, and the annotated
`Document Name-Answer` value, stored in the project as `contract_title`.

Empty clause entries were removed, surrounding whitespace was stripped, and
letter case was left unchanged. The 20 labels and their reporting order were
then frozen. They were not recomputed from the held-out data, and no category
was added, merged, or removed after evaluation.

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

There was no document-title-group overlap between the partitions, and every
class was represented in all three. The grouping field is not a verified
contract identifier, however. Different contracts may share a generic title,
while standard legal language may recur across differently named documents.
For that reason, exact and near-duplicate text was audited separately. These
audits were diagnostic: records were not removed automatically merely because
their wording was repeated.

## 3.4 Compared methods

### 3.4.1 TF-IDF and logistic-regression baseline

The classical baseline represented each clause with TF-IDF-weighted unigrams
and bigrams. The vocabulary was limited to 5,000 features. A logistic-regression
classifier used balanced class weights, a maximum of 1,000 iterations, and
random seed 42. It was implemented with scikit-learn (Pedregosa et al., 2011).
This method generated one of the 20 labels directly and could not produce an
unknown textual response.

### 3.4.2 Zero-shot prompting

The zero-shot method used `mistralai/Mistral-7B-Instruct-v0.2` without updating
its parameters. Mistral 7B is an instruction-capable seven-billion-parameter
model that uses grouped-query and sliding-window attention (Jiang et al., 2023).
Each clause was supplied with the complete class list and an instruction to
return only one category name. Inputs were tokenised to a maximum of 4,096
tokens, generation was limited to 12 new tokens, and decoding was
deterministic.

### 3.4.3 Original PEFT

The original PEFT method adapted the same Mistral model with Low-Rank
Adaptation. LoRA freezes the pretrained weights and learns low-rank update
matrices, reducing the number of trainable parameters (Hu et al., 2022). The
base model was loaded in four-bit NF4 form with double quantisation, following
the memory-saving principles of QLoRA (Dettmers et al., 2023).

The adapter used rank 16, `lora_alpha` 32, dropout 0.05, and the `q_proj`,
`k_proj`, `v_proj`, and `o_proj` target modules. Training used one epoch, a
learning rate of 0.0002, effective batch size 16, seed 42, and 2,048-token
training sequences. There were 13,631,488 trainable parameters, representing
approximately 0.1879% of the 7,255,363,584 total parameters.

In the original run, loss was calculated across the complete formatted
sequence rather than only the target label. The prompt used to create the PEFT
training records asked for classification into the correct clause type but did
not display the 20 possible labels. At inference, the model received a
differently worded instruction containing the full label list. This mismatch
was not recognised until the original test predictions had been inspected. It
is therefore treated as a defect in the original implementation, not as a
prespecified experimental factor.

Original PEFT inference used a 4,096-token input limit and a 12-token
generation limit. These inference limits differ from the 2,048-token maximum
used to construct training sequences and are reported separately rather than
being treated as one shared truncation setting.

### 3.4.4 Retrieval-augmented generation

The RAG method embedded the training clauses with
`sentence-transformers/all-MiniLM-L6-v2`. Sentence-transformer models produce
fixed-size semantic representations suitable for similarity search (Reimers and
Gurevych, 2019). The unnormalised vectors were stored in a FAISS `IndexFlatL2`
index (Johnson et al., 2019). For each query, the three nearest training
examples were inserted into the classification prompt. This implementation
used retrieval as in-context evidence rather than jointly training the
retriever and generator; it is therefore a task-specific RAG pipeline rather
than the end-to-end architecture introduced by Lewis et al. (2020).

Within each RAG prompt, every retrieved training clause was capped at 550
tokens. The query clause was capped at 1,500 tokens; for a longer query, 75% of
the retained tokens came from its beginning and 25% from its end. The assembled
prompt was then left-truncated to the model's 4,096-token input limit.
Generation was deterministic and limited to 12 new tokens.

### 3.4.5 PEFT-RAG hybrid

The hybrid method combined the original LoRA adapter with the three retrieved
examples used by RAG. No additional training was performed. Because the
original adapter had not been trained on retrieval-style prompts, the hybrid
tested whether retrieved demonstrations helped at inference time; it did not
test a retrieval-aware fine-tuning objective.

The hybrid used the same three-neighbour retrieval records and the same 550,
1,500 and 4,096-token truncation rules as RAG. Its generation limit was also 12
new tokens.

## 3.5 Corrected PEFT sensitivity study

### 3.5.1 Controlled answer-only training

The sensitivity adapter retained the original data, training-prompt wording,
base model, LoRA configuration, learning rate, effective batch size, seed, and
one-epoch schedule. Its intended intervention was the loss calculation.
Instruction and clause tokens were assigned the ignore index `-100`; only the
category answer and end-of-sequence token contributed to the causal
language-model loss. Prompts were tokenised with `add_special_tokens=False`
because the chat template already supplied a beginning-of-sequence token.

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

The selection metric was validation Macro F1; accuracy was used only to break a
tie. For interpretation, an absolute Macro-F1 change of 0.01, or a pronounced
class-level recovery or collapse, was treated as material. Condition C achieved
the highest validation Macro F1 and was frozen before the test evaluation. The
diagnostic changed only inference conditions: it did not retrain the adapter.

Condition C used the instruction “Classify the following contract clause into
its correct clause type”, followed by the clause and the output-format
instruction. Unlike the label-list prompt, it did not include the 20 class names
in the inference prompt. This matched the prompt seen during v4 training.

### 3.5.3 Frozen corrected test evaluation

Condition C was evaluated once on all 1,850 test rows. The base model, adapter,
prompt, tokenisation, 4,096-token input limit, deterministic decoding, 12-token
generation limit, and strict parser were frozen beforehand. Alternative prompt
conditions were not evaluated on the test set, and no further model selection
was permitted after the corrected test predictions were inspected.

## 3.6 Output parsing and failure handling

Generated responses were assessed with a strict parser. A response was accepted
only when its complete cleaned text matched one frozen label. Cleaning allowed
differences in letter case, surrounding quotation or Markdown characters, an
optional `Category:` prefix, and terminal punctuation. Explanations, multiple
labels, truncated labels, synonyms, and all other non-canonical outputs were
mapped to `Unknown` and counted as incorrect. Thus, `Unknown` describes an
invalid model response; it is not a twenty-first clause category.

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
resampling (Efron and Tibshirani, 1993).

Exact McNemar tests with Holm correction were retained as descriptive paired
row-level checks. Their p-values were not treated as the main inferential
evidence because the independence assumption is questionable for clauses
nested within 57 groups (McNemar, 1947; Holm, 1979).

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
The original environment was not captured completely, so package versions that
cannot be recovered from saved metadata are not reconstructed from memory. The
corrected PEFT notebooks record the library versions available during those
runs. Together, the notebooks, prediction files, adapter metadata, statistical
outputs, and repository checks form the reproducibility record. The modular
`src/` package was written after the experiments to organise reusable code; it
is a result-preserving refactor, not the path through which the reported LLM
experiments were originally executed.

