# Chapter 7 - Conclusion

## 7.1 Study overview

This thesis compared a TF-IDF logistic-regression baseline with Zero-shot
prompting, Original PEFT, RAG and a PEFT-RAG Hybrid on a grouped 20-class CUAD
subset. Corrected PEFT was analysed separately after weaknesses in the original
implementation were diagnosed. Macro F1 was primary, supported by Accuracy,
class-level results, output-validity checks and document-title-group bootstrap
intervals.

## 7.2 Answers to the research questions

### 7.2.1 RQ1: comparative classification performance

In the original comparison, TF-IDF with logistic regression ranked first,
followed by the Hybrid and RAG; Zero-shot prompting and Original PEFT were
substantially weaker (Table 4.1). Corrected PEFT later achieved the highest
observed scores and exceeded the baseline, but Table 4.3 reports it separately
because its design followed inspection of the original PEFT behaviour.

### 7.2.2 RQ2: class variation and error patterns

Performance varied sharply by clause type. Corrected PEFT was strongest on
categories with distinctive wording but weakest on Non-Transferable License,
Effective Date and Exclusivity (Table 4.6 and Figure 4.2). Conflicting labels
for identical clause strings, especially bare dates and licence-related
language, indicate that some errors arose from missing context rather than
model capacity alone.

### 7.2.3 RQ3: the addition of retrieved examples

Retrieval substantially improved the prompted base model and the Original PEFT
system. RAG increased Macro F1 by 0.1190 over Zero-shot prompting, while the
Hybrid increased it by 0.1504 over Original PEFT. The Hybrid exceeded RAG by
only 0.0002 Macro F1, so the experiment provides little evidence that attaching
the Original adapter added class-balanced performance beyond retrieval itself.

### 7.2.4 Exploratory RQ4: corrected PEFT sensitivity

Removing the duplicate BOS token produced a small validation change, whereas
using the training-matched prompt raised validation Macro F1 to 0.8550 (Table
4.2). The selected configuration reached 0.8460 Macro F1 and 0.8946 Accuracy on
test. This indicates that supervision and inference alignment materially
affected PEFT, but the design cannot isolate the contribution of each change.

## 7.3 Contributions

The thesis contributes an aligned five-method comparison, an explicitly
separated Corrected PEFT sensitivity study, and an evaluation protocol that
retains invalid outputs, audits row alignment, resamples document-title groups
and examines exact-text conflicts. Preserving both PEFT runs makes the
methodological correction visible instead of replacing the original result.

## 7.5 Final conclusion

TF-IDF logistic regression was the best original method, Corrected PEFT was the
best observed configuration, and RAG provided the clearest gain without model
training. The study indicates that legal clause-classification results depend
on the information in the input, the training target, prompt and token handling,
retrieval quality, parsing rules and dependence within the data. Method names
alone do not determine performance.
