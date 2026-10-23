# Chapter 1 - Introduction

## 1.1 Background and motivation

Contracts organise commercial relationships by defining rights, obligations,
restrictions, remedies and events that may alter or end an agreement. Reviewing
these documents is therefore not a simple search for isolated keywords. A
reviewer must identify the function of a passage, distinguish related legal
concepts and recognise when similar wording has a different meaning in its
document context. This work is time-consuming when large collections of
contracts must be examined, and it has become an important application area
for natural language processing (NLP).

Legal NLP has advanced from sparse lexical representations and conventional
machine-learning classifiers to pretrained language models and generative
large language models. Datasets such as LEDGAR, CUAD and the broader LexGLUE
benchmark have made it possible to evaluate models on contract provisions and
other legal-language tasks (Tuggener et al., 2020; Hendrycks et al., 2021;
Chalkidis et al., 2022). These resources also expose difficulties that are easy
to hide in general-domain benchmarks. Legal categories may overlap, standard
clauses are repeatedly reused, class frequencies are uneven, and the meaning
of a short provision may depend on its heading or surrounding agreement.

Large language models offer several ways to approach this setting. A model can
be instructed through a prompt without updating its parameters. It can be
adapted with a relatively small set of trainable parameters, or supplied with
similar labelled examples retrieved at inference time. These approaches differ
in the supervision they require, the information available at prediction time
and the risk of producing responses outside a fixed label set. Their relative
value cannot be inferred from model size alone. Studies of legal-language
models have repeatedly shown that improvements observed on general tasks do not
transfer uniformly to specialised legal problems (Chalkidis et al., 2020;
Hakimi Parizi et al., 2023).

This thesis examines that problem through contract clause classification. Each
input is an extracted contractual passage and the required output is one of 20
legal clause categories. The study compares a supervised TF-IDF
logistic-regression baseline with four uses of the same general-purpose
instruction model: zero-shot prompting, parameter-efficient fine-tuning
(PEFT), retrieval-augmented generation (RAG), and a hybrid that combines the
PEFT adapter with retrieved demonstrations. A later corrected PEFT experiment
is retained separately as a post-hoc sensitivity analysis.

## 1.2 Research problem

The practical question is not whether a large language model can generate a
plausible description of a clause. The task requires a reliable decision from
a closed taxonomy. A useful system must choose the correct category across
both common and uncommon classes and must return output that can be mapped to
the schema without discretionary repair. This makes classification quality and
output validity equally relevant.

Published work provides reasons to expect advantages from each adaptation
strategy, but it does not yield a predetermined ranking. Prompting avoids task-
specific training and can exploit instruction-following behaviour, yet results
can be sensitive to wording, demonstrations and response format (Brown et al.,
2020; Liu et al., 2023). LoRA reduces the number of trainable parameters needed
for fine-tuning, but its success still depends on the training target and on
agreement between training and inference (Hu et al., 2022). Retrieval can add
relevant examples without changing model weights, although its benefit depends
on retrieval quality and the generator's use of the retrieved material (Lewis
et al., 2020). A sparse supervised baseline may remain difficult to beat when
labels are associated with recurring legal terminology.

Comparisons are also vulnerable to methodological distortion. Clauses from the
same contract may leak across row-level splits, malformed generated answers may
be silently discarded, and repeated boilerplate may make test examples closer
to the training material than they first appear. In this study, all systems are
therefore evaluated on one frozen label space and one grouped partition, with
aligned predictions and a common scoring policy. The aim is not to demonstrate
that one family of methods is universally superior. It is to determine how the
implemented strategies behave under the same legal classification conditions
and to explain the main limitations of that comparison.

## 1.3 Research aim and objectives

The aim of the thesis is to empirically compare prompting,
parameter-efficient fine-tuning, retrieval-augmented generation and a hybrid
PEFT-RAG approach for legal contract clause classification, using TF-IDF
logistic regression as a supervised baseline.

The study pursues five objectives:

1. Construct a reproducible 20-class classification dataset from CUAD and
   divide it into grouped training, validation and test partitions;
2. implement the classical baseline and the four Mistral-7B-Instruct-v0.2
   configurations under a common label schema and evaluation protocol;
3. compare overall performance, class-level behaviour and the validity of
   generated outputs;
4. examine the contribution and limitations of retrieved demonstrations,
   including retrieval quality and exact-text overlap; and
5. investigate, as a post-hoc sensitivity analysis, how a corrected PEFT
   configuration behaves when answer-only supervision and matched training and
   inference formatting are used.

The fifth objective is exploratory. It was introduced after the behaviour of
the original PEFT system had been inspected and is not presented as part of the
original fixed comparison.

## 1.4 Research questions

The thesis addresses the following questions:

**RQ1.** How do prompting, parameter-efficient fine-tuning,
retrieval-augmented generation, and a hybrid PEFT-RAG approach compare with
TF-IDF logistic regression in legal contract clause classification
performance?

**RQ2.** How does classification performance vary across clause types, and
what error patterns are associated with the weakest-performing categories?

**RQ3.** What changes in classification performance are observed when
retrieved examples are added to the prompted base model and to the
PEFT-adapted model?

**Exploratory RQ4.** How does PEFT performance change in a post-hoc sensitivity
analysis using answer-only supervision and aligned training and inference
formatting?

The first three questions organise the primary comparison and error analysis.
RQ4 is distinguished from them because it arose from diagnosis of the original
PEFT experiment and is therefore exploratory rather than confirmatory.

## 1.5 Scope and contributions

The empirical scope is deliberately narrow. The data are an English-language,
20-category subset derived from CUAD. The generative experiments use one model
family, Mistral-7B-Instruct-v0.2, and treat each extracted clause as the main
textual input. Named entity recognition, additional legal datasets, unseen
label evaluation and cross-jurisdiction transfer are outside the final scope.
The study also does not claim a controlled comparison of monetary cost, energy
use or latency because those quantities were not collected under a common
measurement protocol.

Within that scope, the thesis makes four contributions. First, it provides an
aligned empirical comparison of classical classification, prompting, PEFT,
RAG and a PEFT-RAG hybrid. Second, it evaluates invalid generative outputs
rather than excluding them from the denominator. Third, it supplements
row-level scores with document-title-group bootstrap intervals and an audit of
identical texts associated with conflicting labels. Finally, it preserves both
the unsuccessful original PEFT result and the later corrected sensitivity run,
making the effect of methodological decisions visible rather than silently
replacing the historical result.

The resulting systems are research prototypes, not substitutes for legal
judgement. Their predictions identify categories within the experimental
schema; they do not determine a clause's enforceability, commercial
acceptability or legal effect.

## 1.6 Structure of the thesis

Chapter 2 reviews legal NLP, contract clause classification and the adaptation
strategies evaluated in the study. Chapter 3 explains the dataset,
partitioning, model configurations, parsing rules and statistical analysis.
Chapter 4 reports the frozen primary results and the corrected PEFT sensitivity
analysis. Chapter 5 interprets the findings, including the classical baseline,
retrieval behaviour, PEFT implementation and data ambiguity. Chapter 6 sets
out the limitations and directions for future work. Chapter 7 answers the
research questions and presents the conclusions.
