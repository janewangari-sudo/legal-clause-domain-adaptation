# Chapter 5 - Discussion

## 5.1 Overview of the findings

The original and sensitivity analyses answer different questions. In the
frozen five-method comparison, TF-IDF with logistic regression ranked first,
while RAG and the Hybrid outperformed Zero-shot prompting and Original PEFT.
Corrected PEFT later produced the highest observed scores, indicating that the
original PEFT outcome depended heavily on supervision and prompt alignment.
Tables 4.1 and 4.3 retain this distinction rather than replacing the historical
result.

## 5.2 Why the classical baseline was difficult to beat

The TF-IDF result is consistent with the structure of this task. Several CUAD
categories contain recurring lexical cues, including “governing law”,
“insurance”, “audit”, and “termination”. A supervised linear classifier can
learn these associations directly. It also returns one label from a fixed set,
so it cannot lose credit by explaining an answer, truncating a label, or
producing two labels.

This does not establish that linear models are generally superior to language
models. The advantage was observed on one split of one English-language dataset
and on a closed 20-class task. It might not persist when terminology changes,
when the relevant distinction depends on distant context, or when the system
must justify its decision. Even with that qualification, the result exposes a
weakness common in model comparisons: if a competent classical baseline is
omitted, improvements attributed to model scale may simply reflect an easy
label-to-keyword relationship.

## 5.3 Interpreting the corrected PEFT result

Corrected PEFT substantially outperformed Original PEFT and exceeded the
TF-IDF baseline; the paired cluster-bootstrap intervals in Table 4.5 excluded
zero. On validation, removing the duplicate BOS token changed Macro F1 only
slightly, whereas using the training-matched prompt produced a larger
improvement (Table 4.2).

The experiment does not isolate a single cause. The corrected adapter used
answer-only supervision, while the validation diagnostic changed prompt
wording and removed the label list. Because all loss-target and prompt
combinations were not trained, the entire improvement from Original to
Corrected PEFT cannot be attributed to loss masking or prompt alignment alone.

The condition also remains post-hoc. Original test errors motivated the
investigation, although validation-only selection and one frozen corrected test
evaluation limited further test-set selection. The result suggests that the
original pipeline understated PEFT performance, but an independently specified
replication is needed to test whether the advantage persists.

## 5.4 Retrieval and the Hybrid method

RAG raised Macro F1 from 0.6572 for Zero-shot prompting to 0.7762 and narrowed
the gap to the baseline. The correct label appeared first for 76.54% of queries
and within the top three for 88.00%, although these retrieval measures do not
reveal which demonstration the generator used. There were 102 exact training
and test matches, but removing them changed RAG Macro F1 only from 0.7762 to
0.7739, so exact copying alone does not explain the result.

The Hybrid achieved slightly higher Accuracy than RAG but nearly identical
Macro F1. It also produced fewer invalid outputs. However, it used the Original
adapter, which had not been trained on retrieval-style prompts. Its score
therefore measures an inference-time combination and does not determine the
performance of a retrieval-aware adapter.

## 5.5 Label ambiguity and missing context

The conflict analysis in Section 4.7 identifies a structural limitation of
clause-only input. Bare dates may represent either Agreement Date or Effective
Date, while transfer restrictions can occur inside a broader License Grant.
Identical wording can therefore receive different labels depending on context
that the classifier does not observe.

The deterministic ceiling applies only when identical isolated strings must
receive one label. It is not a general upper bound: section headings,
neighbouring clauses or document metadata may resolve some conflicts. The high
non-conflict performance indicates that missing context and label definition
are major factors in the remaining errors, alongside model limitations.

## 5.6 Output format sensitivity

Allowing a valid leading label increased Zero-shot Accuracy by 0.0135 and RAG
Accuracy by 0.0173 but did not change the overall ranking. Corrected PEFT
produced no unknown outputs. Strict parsing remains primary because it was
fixed for the main comparison; relaxing it after inspecting test responses
would add analytical discretion.

## 5.7 Implications for legal domain adaptation

For a closed task with recurring terminology, a classical supervised model can
be a sensible deployment choice when predictions must stay within a fixed
schema and computational resources are limited. This study did not collect
comparable cost measurements, so it cannot quantify that trade-off.

The PEFT experiments show that rank, scaling factor and learning rate do not
fully define an adapter system. The loss target, prompt, special-token handling,
decoding and parser also affect performance. Retrieval substantially improved
Zero-shot prompting without changing model weights, although its invalid-output
rate shows that relevant demonstrations do not guarantee controlled generation.

Some labels describe a passage's function within the contract rather than its
wording alone. Adding document context and reviewing conflicting supervision
may therefore be more productive than further optimisation of an unchanged
clause-only pipeline.
