# Data contract

The processed split files are expected to contain these columns:

| Column | Meaning |
|---|---|
| `clause_text` | Extracted legal clause text |
| `clause_type` | One of the 20 frozen class labels |
| `contract_title` | Annotated document-title value derived from `Document Name-Answer` |

`contract_title` is a legacy internal column name. It must not be interpreted as
a verified unique contract identifier.

Expected row counts:

| Split | Clauses | Document-title groups |
|---|---:|---:|
| Train | 8,257 | 193 |
| Validation | 833 | 35 |
| Test | 1,850 | 57 |

The source files are intentionally absent from the repository. Validation code
checks required columns, labels, sizes, missing values, and cross-split group
overlap before model execution.
