# Chapter 2 - Literature Review and Theoretical Background

## 2.1 Natural language processing in the legal domain

Legal work is largely mediated through text, but legal language is not simply a
larger version of general prose. Statutes, judgments and contracts use
specialised vocabulary, defined terms, cross-references and conventional forms
whose interpretation depends on institutional and document context. The same
surface expression may perform different legal functions, while small changes
in modality, scope or exceptions can alter the effect of an otherwise familiar
clause. These features make legal NLP a domain-adaptation problem as well as a
language-understanding problem.

Domain adaptation concerns the transfer of a model or representation learned
under one distribution to a more specialised target setting. In legal NLP, the
source is often broad general-language pretraining and the target is a legal
task with comparatively limited labelled data. Adaptation may occur through
additional domain pretraining, supervised fine-tuning, parameter-efficient
updates, prompting or the introduction of retrieved material at inference.
These mechanisms are not interchangeable. Fine-tuning changes model
parameters, prompting changes the immediate instructions and examples, and
retrieval changes the information available for a particular prediction.

The development of LEGAL-BERT illustrates both the value and difficulty of
domain-specific adaptation. Chalkidis et al. (2020) compared using a general
BERT model directly, continuing its pretraining on legal corpora and
pretraining legal models from scratch. Their results showed that common
adaptation guidelines did not transfer uniformly across legal tasks and led to
a family of legal-domain BERT models. LexGLUE later provided a standardised
collection of legal-language understanding tasks and found consistent benefits
from legal-oriented models across several datasets (Chalkidis et al., 2022).
These findings support domain adaptation, but they do not imply that every
specialised model or adaptation procedure will outperform a general model in
every legal setting.

Legal evaluation must also distinguish linguistic prediction from legal
judgement. LegalBench contains 162 tasks across six forms of legal reasoning
and was developed with substantial input from legal professionals (Guha et
al., 2023). Its breadth shows that legal capability is not a single construct.
Contract clause classification is narrower: it asks whether a passage belongs
to a defined category, not whether a model can advise on enforceability or
resolve a dispute. Narrower tasks are easier to score consistently, but their
results should not be generalised into claims about legal reasoning as a whole.

## 2.2 Contract clause classification

Clause classification assigns one or more functional labels to passages from
contracts. It can support document review by directing attention to provisions
such as governing law, termination, exclusivity, liability or assignment. The
task differs from information extraction: classification chooses a category
for a supplied passage, whereas extraction must first locate the relevant span
within a larger document. It also differs from question answering, although a
dataset created for extraction can be transformed into a classification table
when annotated spans and category names are available.

LEDGAR is an influential contract-provision classification resource. It was
constructed from public filings and contains almost 100,000 provisions drawn
from more than 60,000 contracts, with a very large and noisy label inventory
(Tuggener et al., 2020). The authors examined sampling and noise-removal
strategies and also considered transfer to contracts outside the source
corpus. LEDGAR demonstrates the scale available from document headings and
public filings, but its semi-automatic construction and extreme label space
create a different setting from a smaller expert-annotated taxonomy.

CUAD was created specifically for contract review with annotations supervised
by legal experts. The original resource contains more than 13,000 annotations
from 510 commercial contracts and covers 41 categories considered relevant to
transactional review (Hendrycks et al., 2021). CUAD was introduced primarily as
a span-identification benchmark: models highlight text that a human reviewer
should inspect. The present thesis instead converts selected annotated answers
into a 20-class clause-classification task. Consequently, results in this study
are not directly comparable with CUAD's original extraction scores.

The distinction matters because evaluation choices define the difficulty of a
classification problem. A row-level random split can distribute clauses from
one contract across training and test data. Repeated boilerplate can then make
test performance partly reflect exposure to closely related wording. Grouping
by document or another reliable provenance identifier is therefore preferable
when the research question concerns transfer to unseen documents. Even grouped
splits do not remove all overlap: standard legal language legitimately recurs
across contracts, and public templates can produce exact matches in documents
that are otherwise independent.

Class imbalance presents a second problem. Accuracy weights each row equally,
so a model can obtain a high score by performing well on frequent classes while
failing on small categories. Macro F1 gives every class equal weight and is
therefore useful for fixed legal taxonomies, although it can be unstable when
supports are very small. Per-class precision, recall and F1 remain necessary
to determine whether an aggregate difference is broad or concentrated in a few
labels. For generative classifiers, evaluation must additionally specify what
happens when the model produces an explanation, a synonym, multiple labels or
an incomplete class name.

## 2.3 Large language models and prompting

Prompt-based classification represents a task as natural-language
instructions and requests an output from a pretrained language model. Brown et
al. (2020) demonstrated that sufficiently large autoregressive models can
perform many tasks from instructions and a small number of in-context examples
without parameter updates. Instruction tuning subsequently improved zero-shot
transfer by training models across collections of tasks expressed through
natural-language instructions (Wei et al., 2022). These developments made it
possible to use one model for classification by describing the task rather
than attaching and training a dedicated classifier.

The prompt is nevertheless part of the model configuration. It defines the
available labels, the expected output, the demonstrations and the placement of
the input. Liu et al. (2023) describe prompt-based learning as a process that
transforms an input through a template into text from which the model's output
is mapped back to a task prediction. This mapping can fail even when a response
contains a plausible answer. For a closed-label classifier, “Governing Law”
and “Governing Law, because ...” may communicate the same decision to a person
but differ under an exact parser. Output constraints and parsing rules must
therefore be reported alongside the prompt.

Legal prompting research cautions against assuming that techniques successful
on general benchmarks will transfer unchanged. Hakimi Parizi et al. (2023)
compared zero-shot, few-shot, ensemble, chain-of-thought and other prompting
strategies for legal text classification and concluded that not all models or
prompting approaches were well suited to long, domain-specific professional
documents. Jayakumar et al. (2023) compared general-purpose LLMs on the LEDGAR
subset of LexGLUE and reported lower macro- and micro-F1 than smaller models
fine-tuned for the legal domain. These studies do not establish that prompting
must underperform, but they show why legal results need task-specific
evaluation rather than extrapolation from broad language-model benchmarks.

Prompting has practical advantages: it avoids task-specific training, permits
rapid revision of instructions and can incorporate demonstrations at
inference. Its weaknesses are equally relevant. Prompts consume context,
outputs can depart from the required schema, and apparently minor formatting
choices may change tokenisation or model behaviour. A zero-shot result should
therefore be interpreted as the performance of a model-prompt-decoding-parser
system, not as an intrinsic measure of the underlying language model.

## 2.4 Parameter-efficient fine-tuning

Full fine-tuning updates all parameters of a pretrained model. This can adapt a
model closely to a labelled task but becomes demanding as model size grows, and
storing a complete copy for every task is inefficient. Parameter-efficient
fine-tuning instead updates a small subset of parameters or introduces compact
trainable modules while leaving most pretrained weights frozen.

Low-Rank Adaptation (LoRA) is based on the proposition that the task-specific
weight update can be represented in a lower-dimensional subspace. Rather than
optimising a full update matrix, LoRA learns the product of two smaller
matrices whose rank is much lower than the original dimension. Hu et al.
(2022) showed that this design can sharply reduce trainable parameters and
memory requirements while remaining competitive with full fine-tuning across
several model families. The trained adapter can be stored separately from the
base model, which is attractive when multiple specialised tasks share one
backbone.

QLoRA extends this approach by backpropagating through a frozen, four-bit
quantised model into LoRA adapters. Its technical contributions include the
NormalFloat 4-bit representation, double quantisation and paged optimisers,
which reduce memory use enough to adapt large models on more limited hardware
(Dettmers et al., 2023). Quantisation makes PEFT accessible, but it does not
remove the need to define the supervised target correctly.

For causal language models, a training example often contains an instruction,
the input and the expected answer in one token sequence. If loss is calculated
over the full sequence, the model is trained to reproduce prompt tokens as well
as the answer. Answer-only supervision masks the instruction and input tokens
so that optimisation focuses on the desired completion. Neither choice is
universally correct, but the decision affects what the adapter learns. Prompt
templates, special tokens and inference formatting must also agree with the
training representation. LoRA rank and learning rate alone are insufficient to
describe a reproducible PEFT system.

PEFT should therefore be understood as an adaptation mechanism rather than a
guarantee of improved classification. Small datasets may not cover all label
boundaries, imbalanced supervision may favour common categories, and a
misaligned training objective can produce low validation loss without the
desired inference behaviour. Comparison with prompting is meaningful only when
both pipelines use compatible task definitions and output rules.

## 2.5 Retrieval-augmented generation

Retrieval-augmented generation combines a generator's parametric representation
with information selected from an external collection. Lewis et al. (2020)
formulated RAG for knowledge-intensive NLP by coupling a neural retriever with
a sequence generator. Dense retrieval represents queries and candidate
passages as vectors so that semantically related items can be selected through
nearest-neighbour search. Sentence-BERT provides an efficient architecture for
producing semantically meaningful sentence embeddings (Reimers and Gurevych,
2019), while FAISS supplies scalable similarity-search structures for dense
vectors (Johnson et al., 2019).

In a classification setting, retrieved items can function as demonstrations
rather than factual documents. A query clause is embedded, similar labelled
training clauses are retrieved, and their text-label pairs are placed in the
prompt. This converts a fixed few-shot prompt into an instance-specific one.
The approach requires no update to the generator and can expose a model to
domain terminology at inference time. It also makes part of the decision path
auditable because the retrieved examples can be inspected.

Retrieval quality places an upper constraint on this mechanism. If the nearest
examples carry an irrelevant label, the generator may be anchored to the wrong
category. Even when the correct label appears among the neighbours, the model
may ignore it, copy an inappropriate demonstration or return more than one
answer. Recall at a chosen retrieval depth and top-one retrieved-label accuracy
are therefore useful supporting measures, but they do not replace end-to-end
classification metrics.

Data overlap requires particular care. An exact training-test match may
legitimately arise from standard boilerplate, but it can make retrieval appear
stronger than it would be on novel drafting. Removing every repeated clause
would also distort the domain. A transparent evaluation should report exact
matches, restrict the index to the training partition and test whether results
remain similar when matched cases are excluded. Near-duplicate detection is
harder because small textual differences can be legally material.

The system evaluated in this thesis is best described as retrieval-augmented
in-context classification. It uses a fixed sentence encoder and nearest-
neighbour index to add three labelled examples to an instruction model. It does
not jointly train the retriever and generator and does not claim to reproduce
the architecture of the original RAG paper exactly.

## 2.6 Combining retrieval and parameter adaptation

Retrieval and PEFT address different limitations. Retrieval supplies
instance-specific external context, whereas PEFT changes the model's behaviour
through learned parameter updates. In principle, a hybrid can benefit from
both: the adapter can learn the task and output schema while retrieval provides
local examples for a particular clause. In practice, the two components may
interfere. Demonstrations lengthen the prompt, alter the input distribution and
may conflict with patterns learned during fine-tuning.

This interaction makes the training format important. An adapter trained only
on instruction-and-clause prompts has not learned how to interpret prompts
containing three retrieved demonstrations. Adding retrieval at inference tests
whether the existing adapter can tolerate and use that new structure; it does
not measure the potential of an adapter trained on retrieval-augmented prompts.
A strong hybrid conclusion would require training examples that reproduce the
retrieval format or a factorial design that separates retrieval, adaptation and
prompt changes.

The literature provides extensive evidence on prompting, fine-tuning and RAG
individually, but fewer controlled legal comparisons hold the base model,
dataset, split, labels and scoring policy constant across all three mechanisms
and their combination. The Hybrid condition in this study is consequently an
empirical comparison of one implemented combination, not a general test of all
possible retrieval-and-adaptation architectures.

## 2.7 Classical text-classification baselines

The growth of pretrained models does not eliminate the need for classical
baselines. TF-IDF assigns greater weight to terms that are frequent in one
document but less common across the collection, producing sparse vectors that
capture discriminative vocabulary (Salton and Buckley, 1988). A linear
logistic-regression classifier learns class-specific weights over these
features and returns a distribution over the fixed labels. Class weighting can
partly counter imbalance during fitting.

This combination is well suited to categories marked by recurring phrases,
defined terms or characteristic legal vocabulary. It is computationally
lighter than generative inference, always returns a member of the trained label
set and provides inspectable feature coefficients. Its limitations are also
clear: bag-of-words features represent local lexical evidence more readily than
long-range meaning, word order or document context. Semantically similar
clauses with different vocabulary may remain distant, while identical strings
cannot be assigned different labels without additional features.

A baseline is valuable precisely because these strengths differ from those of
an LLM. If a complex method cannot outperform a class-weighted sparse model on
the same split, the result may indicate that lexical regularity dominates the
task, that the adaptation pipeline is weak, or both. Treating the baseline as a
serious competitor prevents improvement claims that arise only from comparison
with an untuned generative model.

## 2.8 Research gap and analytical framework

Prior research establishes several relevant findings: legal-domain adaptation
can improve specialised tasks; prompting performance is model- and
task-dependent; LoRA and quantisation reduce the resources required for
fine-tuning; and retrieval can supply external context without updating a
generator. The evidence does not determine which strategy should perform best
on a fixed CUAD-derived multiclass task. Published studies often use different
datasets, taxonomies, model families, prompts and metrics, making their scores
unsuitable for direct ranking.

Three gaps motivate the present comparison. First, there is limited controlled
evidence comparing a strong sparse baseline, zero-shot prompting, LoRA PEFT,
retrieved in-context examples and their hybrid under one legal clause schema.
Second, generative output validity is frequently entangled with substantive
classification performance; a model may recognise a category but fail an
exact interface contract. Third, boilerplate repetition and conflicting labels
can constrain a clause-only classifier independently of model capacity.

The thesis addresses these gaps through a within-study framework rather than a
new model architecture. The independent condition is the implemented
adaptation strategy. The principal outcomes are Macro F1 and Accuracy, with
per-class metrics and unknown-output rates providing diagnostic evidence.
Retrieval measures, exact-text conflict subsets and title-group cluster
bootstrap intervals are used to test whether the headline ranking conceals
important differences in information availability or evaluation structure.

The framework supports comparative conclusions, not universal or causal ones.
Only one dataset subset and one generative backbone are used. The later
Corrected PEFT condition was developed after inspection of the original PEFT
behaviour and is therefore analysed separately. This boundary is necessary for
the study to contribute a credible account of what was observed without
converting an exploratory correction into a prespecified experiment.
