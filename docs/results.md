# Chapter 4 — Results

## 4.1 Prediction audit

All six prediction files contained the expected 1,850 test rows. Row
identifiers, clause text and true labels aligned with the frozen test partition,
and all predicted values belonged to the 20-class schema or the `Unknown`
failure category. The test set comprised 57 document-title groups. Corrected
PEFT is reported as a post-hoc sensitivity condition; the other five methods
form the original comparison.

## 4.2 Original five-method comparison

Table 4.1 reports the frozen original results. TF-IDF with logistic regression
was strongest in this comparison, with Accuracy 0.8605 and Macro F1 0.8131.
Hybrid and RAG formed the next tier. Hybrid had slightly higher Accuracy than
RAG, but their Macro F1 values were almost identical. Zero-shot prompting and
Original PEFT performed substantially worse.

**Table 4.1. Original five-method test results**

| Method | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Unknown |
|---|---:|---:|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | **0.8605** | 0.8178 | 0.8211 | **0.8131** | **0.8559** | 0 |
| Zero-shot | 0.6227 | 0.7343 | 0.6453 | 0.6572 | 0.6615 | 244 |
| Original PEFT | 0.6146 | 0.6713 | 0.6688 | 0.6260 | 0.6199 | 2 |
| RAG | 0.8157 | 0.8445 | 0.7484 | 0.7762 | 0.8315 | 138 |
| Hybrid | 0.8259 | 0.8045 | 0.7934 | 0.7764 | 0.8172 | 1 |

The original conclusion was therefore that retrieval yielded the largest
improvement among the Mistral-based approaches, while the classical baseline
remained strongest overall. The corrected PEFT analysis below qualifies that
conclusion rather than erasing it.

## 4.3 Corrected PEFT validation selection

The answer-only v4 adapter was first evaluated under three validation-only
inference conditions. Removing the duplicate beginning-of-sequence token while
retaining the label-list prompt produced only a small improvement from
Condition A to B. Matching the inference prompt to the training prompt produced
a much larger change.

**Table 4.2. Validation-only corrected PEFT diagnostic**

| Condition | Accuracy | Macro F1 |
|---|---:|---:|
| A: label-list prompt, default BOS handling | 0.8595 | 0.7852 |
| B: label-list prompt, one BOS token | 0.8619 | 0.7922 |
| C: training-matched prompt, one BOS token | **0.9256** | **0.8550** |

The A-to-B Macro F1 difference was 0.0070, below the declared 0.01 materiality
threshold. Condition C improved Macro F1 by 0.0698 relative to A and by 0.0628
relative to B. This indicates that prompt matching, rather than BOS handling
alone, was the dominant remaining inference issue. Condition C was selected by
validation Macro F1 before the corrected test evaluation.

## 4.4 Six-method sensitivity comparison

Corrected PEFT achieved Accuracy 0.8946, Macro F1 0.8460 and Weighted F1
0.8861, with no unknown predictions. Numerically, it was the strongest of the
six reported conditions.

**Table 4.3. Test results with corrected PEFT shown as a sensitivity condition**

| Method | Analysis status | Accuracy | Macro F1 | Weighted F1 | Unknown rate |
|---|---|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | Original comparison | 0.8605 | 0.8131 | 0.8559 | 0.0000 |
| Zero-shot | Original comparison | 0.6227 | 0.6572 | 0.6615 | 0.1319 |
| Original PEFT | Original comparison | 0.6146 | 0.6260 | 0.6199 | 0.0011 |
| RAG | Original comparison | 0.8157 | 0.7762 | 0.8315 | 0.0746 |
| Hybrid | Original comparison | 0.8259 | 0.7764 | 0.8172 | 0.0005 |
| Corrected PEFT | Post-hoc sensitivity | **0.8946** | **0.8460** | **0.8861** | **0.0000** |

This result changes the substantive interpretation of PEFT. The poor Original
PEFT score cannot be treated as evidence that parameter-efficient adaptation
was inherently ineffective for the task. Performance depended strongly on the
training objective and consistency between training and inference formatting.

## 4.5 Cluster-bootstrap uncertainty

Table 4.4 reports percentile intervals from 5,000 paired resamples of the 57
test document-title groups. Corrected PEFT retained the highest point estimates.
Its Accuracy interval was 0.8778–0.9120 and its Macro F1 interval was
0.8235–0.8658.

**Table 4.4. Document-title-group cluster-bootstrap intervals**

| Method | Accuracy | 95% CI | Macro F1 | 95% CI |
|---|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | 0.8605 | [0.8453, 0.8764] | 0.8131 | [0.7973, 0.8251] |
| Zero-shot | 0.6227 | [0.5930, 0.6549] | 0.6572 | [0.6321, 0.6823] |
| Original PEFT | 0.6146 | [0.5864, 0.6449] | 0.6260 | [0.6004, 0.6484] |
| RAG | 0.8157 | [0.7856, 0.8462] | 0.7762 | [0.7521, 0.7985] |
| Hybrid | 0.8259 | [0.8040, 0.8448] | 0.7764 | [0.7567, 0.7912] |
| Corrected PEFT | 0.8946 | [0.8778, 0.9120] | 0.8460 | [0.8235, 0.8658] |

Paired cluster-bootstrap differences are more informative than overlap between
separate intervals. Corrected PEFT exceeded the baseline by 0.0341 Accuracy
(95% CI [0.0230, 0.0460]) and 0.0329 Macro F1 (95% CI [0.0162, 0.0516]). Both
intervals excluded zero. The same was true for every comparison between
Corrected PEFT and an original method.

**Table 4.5. Corrected PEFT minus comparison method**

| Comparison method | Accuracy difference | 95% CI | Macro F1 difference | 95% CI |
|---|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | 0.0341 | [0.0230, 0.0460] | 0.0329 | [0.0162, 0.0516] |
| Zero-shot | 0.2719 | [0.2387, 0.3031] | 0.1888 | [0.1582, 0.2131] |
| Original PEFT | 0.2800 | [0.2514, 0.3104] | 0.2199 | [0.1939, 0.2471] |
| RAG | 0.0789 | [0.0580, 0.1005] | 0.0698 | [0.0460, 0.0926] |
| Hybrid | 0.0686 | [0.0501, 0.0903] | 0.0696 | [0.0447, 0.0980] |

Exact McNemar tests also favoured Corrected PEFT after Holm correction, but
those p-values assumed clause-level independence. They are treated as
descriptive checks rather than the principal evidence.

## 4.6 Corrected PEFT class-level performance

Corrected PEFT exceeded F1 0.90 for 12 of the 20 classes. Parties, Document
Name, Governing Law, Cap On Liability and Insurance were classified especially
well. The weakest categories were Non-Transferable License, Effective Date and
Exclusivity.

**Table 4.6. Corrected PEFT per-class test performance**

| Clause type | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Parties | 0.9976 | 1.0000 | 0.9988 | 418 |
| License Grant | 0.6519 | 0.9035 | 0.7574 | 114 |
| Cap On Liability | 0.9888 | 0.9670 | 0.9778 | 91 |
| Audit Rights | 0.9328 | 1.0000 | 0.9652 | 111 |
| Anti-Assignment | 0.9474 | 0.9558 | 0.9515 | 113 |
| Insurance | 0.9452 | 1.0000 | 0.9718 | 69 |
| Document Name | 0.9895 | 1.0000 | 0.9947 | 94 |
| Agreement Date | 0.6452 | 0.9195 | 0.7583 | 87 |
| Governing Law | 1.0000 | 0.9878 | 0.9939 | 82 |
| Expiration Date | 0.8830 | 0.9881 | 0.9326 | 84 |
| Effective Date | 0.7667 | 0.3108 | 0.4423 | 74 |
| Post-Termination Services | 0.8082 | 0.7867 | 0.7973 | 75 |
| Revenue/Profit Sharing | 0.9753 | 0.9186 | 0.9461 | 86 |
| Minimum Commitment | 0.8939 | 0.9365 | 0.9147 | 63 |
| Exclusivity | 0.6875 | 0.5789 | 0.6286 | 57 |
| Rofr/Rofo/Rofn | 0.8714 | 0.8714 | 0.8714 | 70 |
| Ip Ownership Assignment | 0.9500 | 0.9500 | 0.9500 | 40 |
| Non-Transferable License | 0.7059 | 0.2353 | 0.3529 | 51 |
| Non-Compete | 0.8889 | 0.7059 | 0.7869 | 34 |
| Termination For Convenience | 1.0000 | 0.8649 | 0.9275 | 37 |

The asymmetric Agreement Date and Effective Date recalls show that the model
often preferred Agreement Date when the isolated text was compatible with
either category. A related asymmetry occurred between License Grant and
Non-Transferable License.

## 4.7 Exact-text conflicts

The test set contained 120 unique clause strings associated with more than one
true label. These strings covered 245 rows, or 13.24% of the test set. The
deterministic exact-text ceiling was 0.9330.

Corrected PEFT obtained Accuracy 0.4857 on conflict rows but 0.9570 on the
remaining 1,605 rows. Its Macro F1 was 0.4186 across the 17 labels present in
the conflict subset and 0.9162 across all 20 labels in the non-conflict subset.
Every method deteriorated sharply on conflicting rows. This pattern supports
the interpretation that a material portion of the remaining error arises from
label ambiguity or missing document context, not merely model capacity.

The 0.9330 figure is not a universal ceiling. It applies to a deterministic
classifier that receives the exact isolated clause text and must assign one
label to each identical string.

## 4.8 Parser sensitivity

The leading-valid-label parser increased Zero-shot Accuracy from 0.6227 to
0.6362 and RAG Accuracy from 0.8157 to 0.8330. Their Macro F1 changes were
smaller: 0.0090 and 0.0051 respectively. Original PEFT, Hybrid and Corrected
PEFT were unchanged. Corrected PEFT produced no unknown outputs under either
parser.

Strict parsing remains the primary analysis. The sensitivity result shows that
some Zero-shot and RAG errors were output-format failures, but it does not
justify retroactively replacing the parser after seeing test responses.

## 4.9 Results summary

Three conclusions follow from the final evidence. First, TF-IDF with logistic
regression was the strongest method in the original five-method comparison.
Second, a validation-selected correction to PEFT subsequently achieved the
highest overall test performance, and its advantage over the baseline remained
positive under document-title-group resampling. Third, performance was highly
sensitive to exact-text label conflicts: Corrected PEFT approached 96% Accuracy
on non-conflicting rows but remained below 49% on conflict rows. The results
therefore demonstrate both the potential of carefully configured PEFT and the
limits of classifying legally ambiguous examples from isolated clause text.
