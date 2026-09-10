# Customer Churn Analysis — Detailed Findings

## Purpose

This document records the analysis results, modelling decisions, customer segmentation, retention strategy, and governance controls for the telecom customer churn project.

The analysis uses IBM's Telco Customer Churn dataset and covers exploratory analysis, data preparation, predictive modelling, feature-importance analysis, customer segmentation, and a governance-aware retention advisory.

---

# Part 1 — Exploratory Churn Analysis

## Dataset Overview

* Dataset: IBM Telco Customer Churn
* Total customers: **7,043**
* Target variable: **Churn**
* Overall churn rate: **26.54%**
* Customer identifier: `customerID`

## Churn by Contract Type

| Contract type  | Churn rate |
| -------------- | ---------: |
| Month-to-month |     42.71% |
| One year       |     11.27% |
| Two year       |      2.83% |

Month-to-month customers have substantially higher observed churn than customers on one-year or two-year contracts.

This is an observed association rather than proof of causation. Customers may self-select into contract types based on commitment, satisfaction, pricing, tenure, and other circumstances.

## Churn by Internet Service

| Internet service    | Churn rate |
| ------------------- | ---------: |
| Fiber optic         |     41.89% |
| DSL                 |     18.96% |
| No internet service |      7.40% |

Fiber-optic customers show the highest observed churn rate among the three InternetService groups.

## Tenure and Churn

The Pearson correlation between tenure and churn is:

**-0.352**

The negative correlation indicates that customers with longer tenure tend to have lower churn in this dataset. This is an association and should not be interpreted as proof that increasing tenure directly causes lower churn.

---

# Part 2 — Data Preparation

## Cleaning

The `TotalCharges` column contained **11 blank values**.

Investigation showed that these records corresponded to customers with zero tenure. The blank `TotalCharges` values were therefore converted to **0.0** rather than dropping those customers.

* Blank `TotalCharges`: **11**
* Rows dropped: **0**

## Feature Preparation

The `customerID` field was removed from model features because it is an identifier rather than a useful predictive feature.

The target variable `Churn` was separated from the input features.

Numeric variables included:

* `SeniorCitizen`
* `tenure`
* `MonthlyCharges`
* `TotalCharges`

Categorical variables were encoded using one-hot encoding.

Numeric features were standardized as part of the preprocessing pipeline.

## Leakage Control

The preprocessing pipeline was fitted using the training data only and then applied to the test data.

This prevents information from the test set from influencing preprocessing during model training.

---

# Part 3 — Predictive Modelling

## Models Compared

Two classification models were evaluated:

1. Logistic Regression
2. Random Forest

Model selection was based on **5-fold cross-validation F1 score on the training data**, rather than selecting a model using the test set.

## Model Results

### Random Forest

| Metric                  |                  Result |
| ----------------------- | ----------------------: |
| Test accuracy           |                  76.15% |
| Test precision          |                  53.85% |
| Test recall             |                  71.12% |
| Test F1                 |                  61.29% |
| Test ROC-AUC            |                   0.832 |
| Train accuracy          |                  91.14% |
| Train-test accuracy gap | 14.99 percentage points |

Confusion matrix:

```text
[[807, 228],
 [108, 266]]
```

### Logistic Regression

| Metric        | Result |
| ------------- | -----: |
| Test accuracy | 80.62% |
| Test F1       | 60.61% |
| Test ROC-AUC  |  0.842 |

Logistic Regression achieved higher test accuracy and ROC-AUC, but Random Forest achieved the better F1 score used for model selection.

## Model Selection

Random Forest was selected because its **5-fold training cross-validation F1 score was approximately 62.78%**, compared with the Logistic Regression baseline.

The model was therefore selected using the predefined training cross-validation criterion rather than test-set performance.

## Generalization Risk

The Random Forest achieved 91.14% training accuracy compared with 76.15% test accuracy.

This represents a **14.99 percentage-point train-test accuracy gap**, indicating potential overfitting and a meaningful generalization risk.

The model should therefore be monitored carefully before any production deployment.

---

# Part 4 — Feature Importance and Retention Strategy

## Global Model Signals

The top three Random Forest feature-importance signals are:

| Rank | Feature                   | Importance |
| ---- | ------------------------- | ---------: |
| 1    | `tenure`                  |     0.1297 |
| 2    | `TotalCharges`            |     0.1292 |
| 3    | `Contract_Month-to-month` |     0.1078 |

These are **global model feature-importance signals**, not customer-specific causal explanations.

## Recommended Actions

### 1. Tenure

Prioritize customers during their first 12 months for proactive retention check-ins and consider an annual-contract offer before renewal.

### 2. TotalCharges

Prioritize high-value customers for tailored loyalty outreach and appropriate retention offers.

### 3. Month-to-month Contract

For eligible customers, consider a time-limited annual-contract discount or fee waiver.

These recommendations are business actions based on predictive signals. They should not be interpreted as proof that changing a particular feature will cause a customer to remain.

---

# Part 5 — Customer Segmentation

KMeans clustering was used to create four customer segments using:

* Tenure
* MonthlyCharges
* Predicted churn probability

## Segment Results

| Segment | Business profile                  | Customers | Avg. tenure | Avg. monthly charges | Avg. churn risk | Revenue at risk |
| ------- | --------------------------------- | --------: | ----------: | -------------------: | --------------: | --------------: |
| 0       | New, high-spend, high-risk        |     2,111 |     13.6 mo |               $79.14 |          76.40% |     $127,734.69 |
| 1       | Established, high-spend, low-risk |     1,995 |     56.4 mo |               $92.48 |          22.89% |      $43,540.39 |
| 2       | New, low-spend, high-risk         |     1,729 |     12.5 mo |               $36.10 |          26.86% |      $17,097.02 |
| 3       | Established, low-spend, low-risk  |     1,208 |     54.1 mo |               $34.89 |           6.65% |       $3,352.68 |

## Recommended Campaign

**Segment 0 — New, high-spend, high-risk**

This segment is the recommended first retention campaign because it combines the highest average predicted churn risk with the largest expected monthly revenue at risk.

The campaign should focus on proactive retention outreach during the early customer lifecycle.

---

# Part 6 — Governance-Aware Retention Advisory

## Retention Playbook

The retention advisor uses deterministic rule-based retrieval before any LLM generation.

### Clause 1

**High Risk — probability ≥ 0.70**

Offer a loyalty discount and a callback from a retention specialist within 48 hours.

### Clause 2

**Moderate Risk — 0.40–0.70**

Send a targeted email highlighting an underused service or a contract upgrade offer.

### Clause 3

**New Customer, Any Risk — Tenure < 3 months**

Route the customer to the onboarding team instead of the standard retention flow.

### Clause 4

**Non-Discrimination Rule**

Retention explanations must never state or imply that gender, senior-citizen status, or family/partner status contributed to a customer's risk score.

## Retrieval Priority

For the selected test customer:

* Predicted churn probability: **approximately 99.22%**
* Tenure: **1 month**
* Expected clause: **Clause 3**

Clause 3 takes priority because the customer's tenure is below three months, regardless of the predicted risk probability.

---

# Part 7 — Task 6 LLM Context Control

The LLM is intended to receive only:

1. Risk probability
2. Tenure
3. Retrieved playbook clause
4. Three global feature-importance signal names

The following are not passed to the LLM:

* Customer ID
* Full customer row
* Raw demographic values
* Other unnecessary customer attributes

The purpose of this allowlist is to minimize unnecessary exposure of customer information and prevent protected demographic or family attributes from being used as retention explanations.

## Prompt Governance

The system prompt is designed to require the LLM to:

* Use only the retrieved playbook clause and supplied inputs.
* State the customer's risk probability and tenure.
* Recommend only the action allowed by the retrieved clause.
* Avoid inventing causes, customer facts, or unsupported explanations.
* Never state or imply that gender, SeniorCitizen, Partner, Dependents, or other protected demographic/family attributes caused or contributed to the risk score.

## Output Validation

Generated output should be checked for prohibited demographic/family references before acceptance.

The audit record should retain, where available:

* Retrieved clause
* Permitted input fields
* Generated response
* Validation result

---

# Part 8 — Grounded vs Ungrounded LLM Test

## Expected Clause

For the selected test customer:

**Expected clause: Clause 3**

Reason:

**Tenure = 1 month < 3 months**, so Clause 3 has priority over the high-risk clause.

## Grounded LLM Call

**Status: Pending assignment-approved LLM access.**

The actual LLM response has not been fabricated.

## Ungrounded LLM Call

**Status: Pending assignment-approved LLM access.**

The comparison call must be executed using the same assignment-approved provider after access is available.

## Comparison Requirement

The grounded call should be evaluated against the expected Clause 3 result.

The ungrounded call should be compared with the expected result to determine whether omitting the playbook causes the model to guess, invent, or select an incorrect retention action.

If an ungrounded call happens to produce the correct clause, it should be described as **correct in that run but ungrounded**, rather than automatically calling it a hallucination.

---

# Part 9 — Failure Mode and Governance Risk

Without retrieval grounding, an LLM may generate a retention recommendation that is not supported by the approved playbook.

Potential consequences include:

* Incorrect customer action
* Unsupported explanations
* Compliance exposure
* Inconsistent retention treatment
* Loss of auditability

This risk is particularly important in a retention setting because generated explanations can influence business decisions about customers.

The deterministic retrieval step provides a controlled policy source, while input allowlisting and output validation provide additional governance controls.

---

# Part 10 — Monitoring and Cost Control

## Monitoring

The primary monitoring signal is the difference between predicted and observed churn rates by segment each month.

Potential model drift should be investigated if this gap exceeds an agreed threshold, such as five percentage points, or if recall declines materially.

## Cost Control

The system can reduce LLM usage by:

* Caching deterministic playbook retrieval.
* Using the LLM only for short explanations.
* Batching eligible requests.
* Using an approved lower-cost model for simple standardized cases where appropriate.

---

# Task Completion Status

| Task                                                   | Status                        |
| ------------------------------------------------------ | ----------------------------- |
| Task 1 — Exploratory churn analysis                    | ✅ Completed                   |
| Task 2 — Data preparation                              | ✅ Completed                   |
| Task 3 — Predictive modelling                          | ✅ Completed                   |
| Task 4 — Feature importance                            | ✅ Completed                   |
| Task 5 — Customer segmentation                         | ✅ Completed                   |
| Task 6 — Deterministic retrieval and governance design | ✅ Completed                   |
| Task 6 — Actual grounded LLM call                      | ⏳ Pending approved LLM access |
| Task 6 — Actual ungrounded LLM call                    | ⏳ Pending approved LLM access |

**Important:** No LLM response has been fabricated. The remaining LLM execution should only be marked complete after the assignment-approved provider is actually used and the exact outputs are recorded.

---

# Source Files

* `notebooks/01_analysis.ipynb`
* `src/data_processing.py`
* `src/retention_rag.py`
* `docs/MEMO.md`
* `QUICKSTART.md`

