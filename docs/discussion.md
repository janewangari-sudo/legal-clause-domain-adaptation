# Chapter 5 — Discussion

## 5.1 Overview of the findings

The experiments produced two related but distinct findings. In the original
five-method comparison, TF-IDF with logistic regression achieved the highest
Accuracy and Macro F1. RAG and the PEFT–RAG hybrid substantially improved on
zero-shot prompting and Original PEFT, but neither surpassed the classical
baseline. In the subsequent sensitivity study, Corrected PEFT achieved the
highest overall scores: 0.8946 Accuracy and 0.8460 Macro F1.

These findings are not contradictory. They answer slightly different
questions. The original comparison shows how the five implemented pipelines
performed when first frozen. The sensitivity study shows that the original
PEFT result was highly dependent on training-objective and prompt-consistency
choices. The correct conclusion is therefore not that one method class is
unconditionally superior. It is that implementation fidelity materially
changed the ranking of the methods on this task.

## 5.2 Why the classical baseline was difficult to beat

The strong TF-IDF result is plausible for a fixed-label legal classification
task. Many CUAD categories are associated with recurring lexical patterns,
including terms such as “governing law”, “insurance”, “audit”, and
“termination”. A supervised linear classifier can use these repeated local
signals directly without generating free-form text. It also cannot lose credit
through formatting errors.

The baseline should not be described as generally superior to language models.
Its advantage was observed on one dataset, one split, and a closed 20-class
task. It may weaken when labels depend on wider context, when terminology
changes across jurisdictions, or when the task requires explanation rather
than category assignment. Nevertheless, its performance demonstrates that an
LLM comparison without a serious classical baseline would have overstated the
value of model scale.

## 5.3 Interpreting the corrected PEFT result

Original PEFT obtained 0.6146 Accuracy and 0.6260 Macro F1, whereas Corrected
PEFT obtained 0.8946 and 0.8460 respectively. The paired cluster-bootstrap
intervals for both differences excluded zero. Corrected PEFT also exceeded the
TF-IDF baseline by 0.0341 Accuracy and 0.0329 Macro F1, with positive
document-title-group bootstrap intervals.

The validation diagnostic helps explain part of this change. Correcting the
extra beginning-of-sequence token while retaining the label-list prompt moved
Macro F1 only from 0.7852 to 0.7922. Replacing that prompt with the exact
training prompt increased Macro F1 to 0.8550. The inference-prompt mismatch was
therefore materially more consequential than BOS handling for the completed v4
adapter.

The evidence does not support assigning the entire improvement to one cause.
The v4 adapter used answer-only supervision, whereas the Original PEFT adapter
used full-sequence loss. The later A–C diagnostic changed inference conditions
without retraining and therefore isolated prompt and BOS effects within v4, but
the study did not train all combinations of loss objective and prompt design.
A claim such as “answer-only loss caused the full 0.2199 Macro F1 improvement”
would consequently be unjustified. What can be stated is that the combination
of answer-focused training and matched inference formatting produced a much
stronger PEFT system.

The post-hoc status also matters. Error inspection from the original test run
helped motivate the correction. Validation-only selection and a single frozen
test evaluation reduced further leakage, but they cannot turn the sensitivity
study into a preplanned experiment. Reporting both PEFT versions is therefore
more credible than replacing the initial result with the better one.

## 5.4 Retrieval and the hybrid method

RAG increased Macro F1 from 0.6572 for Zero-shot to 0.7762 and reduced the
performance gap to the baseline. This supports the practical value of supplying
semantically similar labelled examples at inference time. The retrieval audit
also showed that the correct label appeared among the top three retrieved
examples more often than it appeared at rank one, suggesting that multiple
demonstrations gave the generator useful evidence even when the nearest single
example was imperfect.

Hybrid produced slightly higher Accuracy than RAG but almost identical Macro
F1. Its near-zero unknown rate shows that the adapter improved adherence to the
required output format. However, the hybrid did not inherit the full benefit of
Corrected PEFT. It used the Original PEFT adapter, which had not been trained on
retrieval-style prompts. The result therefore concerns inference-time
combination, not retrieval-aware adapter training. A future experiment could
train an answer-only adapter on the same prompt structure used by the hybrid,
but doing that after the frozen test analysis would constitute a new study.

## 5.5 Label ambiguity and missing context

The exact-text analysis revealed a structural limit in the task formulation.
The test set contained 120 clause strings assigned to multiple labels, covering
245 rows. Corrected PEFT achieved 0.9570 Accuracy on non-conflicting rows but
only 0.4857 on conflict rows. All methods showed the same broad deterioration.

Agreement Date and Effective Date illustrate the problem. A bare date such as
“September 28, 2018” does not identify its legal function when removed from the
surrounding document. License Grant and Non-Transferable License can also share
the same language because transfer restrictions may form part of a licence
grant. A clause-only model is forced to infer distinctions that may not be
present in its input.

The calculated 0.9330 ceiling should be interpreted narrowly. It describes the
best deterministic assignment obtainable when every identical text must
receive one label. It does not prove that 93.30% is the maximum achievable
accuracy. Contract title, section heading, neighbouring clauses, or other
document context could distinguish examples that are identical when isolated.

This finding has practical implications. Further optimisation of the same
clause-only model may produce diminishing returns unless the label conflicts
are reviewed or contextual features are introduced. The 0.9570 non-conflict
Accuracy suggests that data definition has become at least as important as
model capacity for the remaining errors.

## 5.6 Output-format sensitivity

Strict parsing penalised valid labels followed by explanations or additional
labels. Allowing a valid leading label increased Zero-shot Accuracy by 0.0135
and RAG Accuracy by 0.0173. The smaller Macro F1 changes indicate that these
formatting failures were meaningful but did not explain the overall method
ranking.

Corrected PEFT was unchanged under the relaxed parser and produced no unknown
outputs. This is evidence that task-specific adaptation improved not only
classification but also compliance with the required response format. The
strict parser remains preferable for the main comparison because it was the
frozen rule and because accepting arbitrary explanatory continuations after
test inspection would introduce analytical discretion.

## 5.7 Implications for legal-domain adaptation

The results suggest four practical lessons.

First, classical supervised models should remain part of legal NLP evaluation
when the task has fixed labels and repeated lexical patterns. Their low
computational cost and strong performance make them a meaningful benchmark,
not a formality.

Second, PEFT quality depends on the complete training-and-inference pipeline.
Adapter rank and learning rate are not sufficient descriptions of an
experiment; prompt construction, token boundaries, supervised-token masking,
and decoding rules can alter the conclusion.

Third, retrieval offers a useful no-training adaptation mechanism. It improved
substantially over Zero-shot and may be preferable when labelled examples are
available but GPU training is impractical. Its strict-parser unknown rate,
however, shows that retrieval does not automatically guarantee controlled
generation.

Fourth, legal labels may encode document function rather than wording alone.
When identical text receives different labels, additional document context or
revised annotation policy may yield more benefit than another round of
hyperparameter tuning.

## 5.8 Threats to validity and future work

The main internal-validity threat is the post-hoc origin of Corrected PEFT. The
validation/test separation and frozen single test evaluation strengthen the
result, but independent replication would provide stronger confirmation. A
future study should specify the prompt, answer-only masking and selection rule
before evaluating any test predictions.

A full factorial design could separately vary full-sequence versus answer-only
loss and label-list versus training-matched prompts. That design would estimate
which component contributes most, rather than attributing the combined change
retrospectively.

Future work should also test document-aware inputs, especially for Agreement
Date, Effective Date, License Grant and Non-Transferable License. Contract
headings or neighbouring text may resolve conflicts that are impossible from
isolated clauses. Evaluation on another legal dataset and another base model
would show whether the observed ranking generalises.

Finally, efficiency should be measured consistently. The corrected adapter
required 2 hours, 16 minutes and 44 seconds of training on the recorded Colab
run, while the classical baseline required no GPU. Complete wall-clock,
inference-latency, memory, energy and financial-cost measurements were not
collected under a common protocol. Claims about cost-effectiveness should
therefore remain qualitative.

## 5.9 Discussion summary

The study initially appeared to show that PEFT underperformed both zero-shot
prompting and retrieval. The controlled sensitivity analysis exposed that this
conclusion was fragile: a corrected PEFT pipeline became the strongest observed
configuration. At the same time, the classical baseline remained highly
competitive, retrieval offered substantial gains without additional model
training, and exact-text conflicts sharply constrained every method. The main
lesson is methodological as much as predictive: credible comparison of legal
language-model adaptation strategies requires strict control over prompts,
training targets, parsing rules, grouped uncertainty and the status of
post-hoc analyses.
