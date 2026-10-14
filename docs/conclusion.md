# Chapter 7 - Conclusion

## 7.1 Study overview

This thesis compared adaptation strategies for legal contract clause
classification on a fixed 20-class subset derived from CUAD. The original
experiment evaluated TF-IDF logistic regression, zero-shot prompting,
parameter-efficient fine-tuning, retrieval-augmented generation and a
PEFT-RAG hybrid on the same grouped test partition. A later answer-only PEFT
adapter and inference-format diagnostic were reported separately as a post-hoc
sensitivity analysis. Macro F1 was the primary metric, supported by Accuracy,
Weighted F1, class-level scores, unknown-output rates and uncertainty intervals
based on document-title-group resampling.

The study was motivated by a practical uncertainty. Prompting, parameter
adaptation and retrieval can all introduce legal-domain information, but they
do so in different ways and create different failure modes. The findings show
that the name of the adaptation strategy is not enough to predict performance.
Training targets, prompt construction, special-token handling, retrieval
quality, parsing and the information contained in the clause itself all
affected the observed outcome.

## 7.2 Answers to the research questions

### 7.2.1 RQ1: comparative classification performance

RQ1 asked how prompting, PEFT, RAG and the Hybrid compared with TF-IDF logistic
regression. In the original five-method comparison, TF-IDF logistic regression
was the strongest method, with 0.8605 Accuracy and 0.8131 Macro F1. Hybrid
followed at 0.8259 Accuracy and 0.7764 Macro F1, while RAG obtained 0.8157 and
0.7762 respectively. Zero-shot prompting reached 0.6227 Accuracy and 0.6572
Macro F1. Original PEFT was lowest on Accuracy at 0.6146 and obtained 0.6260
Macro F1.

The answer to RQ1 is therefore that the classical supervised baseline offered
the best performance in the original fixed comparison. Retrieval-based
methods were the strongest original LLM configurations, but neither surpassed
the baseline. Greater architectural complexity did not produce a corresponding
increase in Macro F1. This ranking applies to the implemented systems and the
selected CUAD subset; it is not evidence that sparse classifiers are generally
superior to language models for legal NLP.

Corrected PEFT produced the highest score observed anywhere in the project:
0.8946 Accuracy and 0.8460 Macro F1. It exceeded the TF-IDF baseline by 0.0341
Accuracy, with a paired cluster-bootstrap 95% interval of [0.0230, 0.0460], and
by 0.0329 Macro F1, with an interval of [0.0162, 0.0516]. This finding changes
the interpretation of PEFT but not the membership of the original comparison.
Corrected PEFT was developed post hoc and cannot be relabelled as a
prespecified primary system.

### 7.2.2 RQ2: class variation and error patterns

RQ2 asked how performance varied across clause types and which error patterns
were associated with weaker categories. Corrected PEFT performed very strongly
on Parties, Document Name, Governing Law, Cap On Liability, Insurance and Audit
Rights. Its weakest F1 scores were for Non-Transferable License (0.3529),
Effective Date (0.4423) and Exclusivity (0.6286). Original methods showed
related difficulties, although their exact class rankings differed.

Two recurring confusions explain part of this variation. Agreement Date and
Effective Date often contain bare dates whose function is not recoverable from
the isolated string. License Grant and Non-Transferable License can also share
wording because transfer restrictions may form part of a broader grant. In the
test partition, 245 rows contained one of 120 exact clause strings associated
with more than one label. Corrected PEFT achieved 0.4857 Accuracy on those rows
and 0.9570 on the remaining 1,605 rows.

Output formatting created another error source. Under the strict parser,
Zero-shot produced 244 unknown responses and RAG produced 138. Accepting a
valid leading label improved their Accuracies by 0.0135 and 0.0173, but did not
change the overall ranking. Corrected PEFT produced no unknown responses and
was unchanged by the relaxed parser. The answer to RQ2 is consequently that
weak classes reflected both semantic ambiguity in clause-only inputs and
method-specific output failures. Not every error can be attributed to model
capacity.

### 7.2.3 RQ3: the addition of retrieved examples

RQ3 asked what changed when retrieved examples were added to the prompted base
model and to the PEFT-adapted model. Adding retrieval to the base model raised
Accuracy from 0.6227 for Zero-shot to 0.8157 for RAG, an increase of 0.1930.
Macro F1 increased from 0.6572 to 0.7762, a gain of 0.1190. Retrieval therefore
provided a substantial benefit over the zero-shot configuration.

The retriever's top-ranked example had the correct label for 0.7654 of test
queries, and the correct label appeared among the top three for 0.8800. Exact
train-test text matches occurred in 102 of 1,850 cases. After those rows were
excluded, RAG still achieved 0.8061 Accuracy and 0.7739 Macro F1, showing that
its improvement was not explained solely by exact copying.

Adding the same retrieved context to Original PEFT raised Accuracy from 0.6146
to 0.8259 and Macro F1 from 0.6260 to 0.7764. This comparison must be treated
carefully because the original adapter had not been trained on retrieval-style
prompts and the Original PEFT pipeline contained the alignment defects examined
later. The Hybrid exceeded RAG by only 0.0103 Accuracy and 0.0002 Macro F1.
Thus, retrieval clearly improved the two non-retrieval configurations, but the
available evidence does not show a material Macro F1 benefit from attaching
the original adapter to RAG.

### 7.2.4 Exploratory RQ4: corrected PEFT sensitivity

RQ4 asked how PEFT performance changed in a post-hoc sensitivity analysis using
answer-only supervision and aligned training and inference formatting. The
answer-only adapter was first evaluated on validation data under three frozen
inference conditions. The existing label-list prompt with default tokenisation
obtained 0.7852 Macro F1. Removing the duplicate start-token effect increased
it to 0.7922. Using the exact training prompt with one start token increased
validation Macro F1 to 0.8550 and Accuracy to 0.9256. That condition was
selected before the single corrected test evaluation.

The selected configuration obtained 0.8460 Macro F1 and 0.8946 Accuracy on the
test set, compared with 0.6260 and 0.6146 for Original PEFT. The sensitivity
analysis therefore demonstrates that PEFT performance was highly dependent on
the implemented supervision and on alignment between training and inference.
It does not establish how much of the improvement was caused by answer-only
loss, prompt wording or another associated change, because the study did not
train every combination in a complete factorial design.

## 7.3 Contributions

The empirical contribution is an aligned comparison of five primary systems on
one legal classification task, accompanied by a separately labelled corrected
PEFT sensitivity analysis. The comparison shows that a classical sparse model
can remain a strong benchmark, that retrieved demonstrations can substantially
improve an untuned generator, and that a poorly aligned PEFT pipeline can hide
the potential of the adaptation method.

The methodological contribution lies in the treatment of evaluation details as
part of the experiment. Generated outputs were assessed under a frozen strict
parser, prediction files were audited row by row, and uncertainty was estimated
by resampling document-title groups rather than treating every clause as
independent. The exact-text conflict analysis further demonstrated that some
class distinctions cannot be resolved reliably from isolated clause wording.

The reproducibility contribution is the preservation of the data-processing
logic, executed notebooks, prediction records, metrics, adapter metadata and
statistical outputs. The original PEFT result was not overwritten when the
corrected experiment succeeded. This makes the evolution of the analysis
auditable and prevents the final account from presenting exploratory work as
though it had been planned from the outset.

## 7.4 Unmet objectives and future direction

The study does not establish comparative cost efficiency. Corrected PEFT
training time was recorded, but runtime, energy, memory and financial cost were
not measured under a common protocol for all methods. It also does not test
generalisation to unseen clause types, another dataset, another language or an
out-of-domain contract collection. These objectives appeared in the early
project concept but were not demonstrated by the final experiment and should
not be inferred from the grouped test result.

An independently specified replication should freeze Corrected PEFT before any
test inspection and cross loss masking with prompt format in a complete design.
A retrieval-aware adapter should be trained on the same kind of demonstrated
prompts it will receive at inference. Data-focused work should inspect
conflicting annotations against their source contracts and evaluate section
headings, neighbouring provisions and document metadata. Broader datasets and
model families would then be needed before making general claims about legal-
domain adaptation.

## 7.5 Final conclusion

Within this study, the best original method was TF-IDF logistic regression and
the best observed configuration was the post-hoc Corrected PEFT system. RAG
offered the clearest improvement without model training, while the Hybrid added
little Macro F1 beyond RAG. The apparent failure of Original PEFT was not a
simple property of LoRA; it was closely tied to how the target, prompt and
tokenisation were implemented.

The broader conclusion is that legal-domain adaptation cannot be judged from a
method label alone. A reliable comparison must account for what information is
available in the input, what the model is trained to predict, how inference is
formatted, how generated outputs are converted into labels and how dependence
within the data is handled. In this experiment, those choices were as important
to the final result as the distinction between prompting, retrieval and
fine-tuning.
