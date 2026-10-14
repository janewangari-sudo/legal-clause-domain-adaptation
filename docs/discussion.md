# Chapter 5 - Discussion

## 5.1 Overview of the findings

The experiments produced two related but distinct findings. In the original
five-method comparison, TF-IDF with logistic regression achieved the highest
Accuracy and Macro F1. RAG and the PEFT-RAG hybrid substantially improved on
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

Original PEFT obtained 0.6146 Accuracy and 0.6260 Macro F1, whereas Corrected
PEFT obtained 0.8946 and 0.8460 respectively. The paired cluster-bootstrap
intervals for both differences excluded zero. Corrected PEFT also exceeded the
TF-IDF baseline by 0.0341 Accuracy and 0.0329 Macro F1, with positive
document-title-group bootstrap intervals.

The validation diagnostic accounts for part of this change. Correcting the
extra beginning-of-sequence token while retaining the label-list prompt moved
Macro F1 only from 0.7852 to 0.7922. Replacing that prompt with the exact
training prompt increased Macro F1 to 0.8550. The inference-prompt mismatch was
therefore associated with a much larger change than BOS handling for the
completed v4 adapter.

That comparison should not be stretched into a causal decomposition. Condition
C changed the prompt as a whole, including its wording and the absence of the
label list; it did not vary those elements one at a time. More broadly, the
evidence does not support assigning the entire Original-to-Corrected PEFT
improvement to one cause. The v4 adapter used answer-only supervision, whereas
the Original PEFT adapter used full-sequence loss. The later A-C diagnostic
changed inference conditions without retraining, but the study did not train
all combinations of loss objective and prompt design. A claim such as
“answer-only loss caused the full 0.2199 Macro F1 improvement” would therefore
be unjustified. What can be stated is that answer-focused training combined
with matched inference formatting produced a much stronger PEFT system.

The post-hoc status limits the strength of the comparison. Error inspection
from the original test run helped determine which defect to investigate.
Validation-only selection and a single frozen evaluation prevented direct
selection among v4 conditions on the test set, but the wider research question
had already been influenced by test behaviour. Corrected PEFT is therefore
strong evidence that the original implementation understated PEFT performance;
it is weaker evidence that the same advantage would reproduce on an untouched
dataset. Reporting both PEFT versions is more credible than replacing the
initial result with the better one.

## 5.4 Retrieval and the hybrid method

RAG increased Macro F1 from 0.6572 for Zero-shot to 0.7762 and reduced the
performance gap to the baseline. This supports the practical value of supplying
semantically similar labelled examples at inference time. The retrieval audit
showed top-one label accuracy of 0.7654 and correct-label Recall@3 of 0.8800.
Multiple demonstrations therefore increased the chance that the prompt
contained an example from the correct class, although these figures do not show
which demonstration the generator actually used.

Exact text overlap is an obvious alternative explanation for retrieval
performance. There were 102 exact train-test matches, but removing them reduced
RAG Macro F1 only from 0.7762 to 0.7739 and Hybrid Macro F1 from 0.7764 to
0.7756. The retrieval results cannot therefore be reduced to those exact
matches. Recurrent legal boilerplate and near-duplicate language may still make
the test distribution easier, so the analysis does not eliminate every form of
template overlap.

Hybrid produced slightly higher Accuracy than RAG but almost identical Macro
F1. Its near-zero unknown rate is consistent with better adherence to the
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
outputs. In this experiment, the corrected adaptation procedure was associated
with both higher classification scores and consistent output formatting. The
strict parser remains preferable for the main comparison because it was the
frozen rule and because accepting explanatory continuations after test
inspection would introduce analytical discretion.

## 5.7 Implications for legal-domain adaptation

For a closed classification task with recurring terminology, a classical
supervised model is not merely a token baseline. It may be the sensible
deployment choice when its accuracy is competitive, predictions must remain
within a fixed schema, and computational resources are limited. The present
study did not collect a common cost benchmark, so it cannot quantify that
trade-off, but the baseline required neither LLM inference nor adapter
training.

The PEFT findings make the definition of an experiment broader than its LoRA
hyperparameters. Rank, scaling factor, and learning rate are only part of the
system. Prompt construction, special-token handling, the tokens included in
the loss, decoding, and parsing all affected the observed result. Reporting an
adapter configuration without these surrounding choices would be insufficient
for reproduction.

Retrieval remains useful when labelled examples exist but training is
impractical. It improved substantially over Zero-shot without changing model
weights. Its 7.46% strict-parser unknown rate also shows the compromise: adding
relevant examples improved classification, but did not guarantee controlled
generation. In an operational system, constrained decoding or a discriminative
classification head might be preferable to repairing outputs after generation.

The conflict analysis raises a more basic issue. Some labels describe the
function of a passage within a contract, not merely its wording. When identical
text is assigned to Agreement Date in one record and Effective Date in another,
the model may be asked to recover information that is absent from the clause.
Adding headings, neighbouring provisions, or document metadata may therefore
be more productive than further tuning a clause-only model. Annotation review
is also necessary, but a repeated text with two labels is not automatically an
annotation error; the same wording can legitimately serve different functions.

## 5.8 Discussion summary

The original experiment suggested that PEFT underperformed both zero-shot
prompting and retrieval. The sensitivity analysis showed that this conclusion
depended on a defective PEFT implementation: the corrected pipeline became the
highest-scoring observed configuration. That result must remain qualified by
its post-hoc origin. The classical baseline was still competitive, retrieval
produced substantial gains without training the generator, and exact-text
conflicts constrained every method. Taken together, the experiments show that
method ranking cannot be separated from prompt design, training targets,
output parsing, grouped uncertainty, and the information contained in the
input itself.
