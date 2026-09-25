# Methodology summary

## Dataset

The study uses CUAD v1 and a frozen set of 20 clause classes. Clause text retains
its original case; surrounding whitespace and empty entries are removed.

## Grouped split

Clauses were partitioned with a two-stage `GroupShuffleSplit`. The grouping
variable was derived from `Document Name-Answer` and stored internally as
`contract_title`. All clauses sharing the same annotated document-title value
were assigned to one partition.

This prevents document-title-group overlap, but it is not proof of unique
contract separation: independent source contracts may share a generic title.
The final partitions contain 8,257 training clauses, 833 validation clauses,
and 1,850 test clauses.

## Methods

1. TF-IDF unigrams and bigrams with balanced logistic regression.
2. Zero-shot classification with Mistral-7B-Instruct-v0.2.
3. LoRA PEFT using rank 16 and alpha 32.
4. RAG using MiniLM embeddings, an unnormalised `IndexFlatL2` FAISS index, and
   three retrieved training examples.
5. A Hybrid using the trained LoRA adapter with the RAG prompt context.

## Evaluation

Macro F1 is the primary metric. Accuracy, Macro Precision, Macro Recall,
Weighted F1, unknown-output rate, per-class metrics, bootstrap confidence
intervals, exact McNemar tests, and paired bootstrap Macro-F1 differences are
also reported. Generated labels outside the frozen schema are mapped to
`Unknown` and scored as incorrect.
