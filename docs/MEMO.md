# Customer Churn Analysis: Executive Memo

**From:** Data Science Team  
**To:** Board and CFO  
**Date:** September 6, 2026  
**Subject:** Predictive churn model and retention strategy

## Executive Summary

The analysis evaluates customer churn using IBM's Telco dataset and combines exploratory analysis, predictive modelling, customer segmentation, and a governance-aware retention advisory design.

The overall churn rate is 26.54%. The analysis identifies new, high-spend, high-risk customers as the recommended first retention campaign because this segment has an average predicted churn risk of 76.40% and approximately $127,734.69 in expected monthly revenue at risk.

The model is predictive rather than causal. Contract type and other model signals should therefore be treated as associations and prioritization signals, not proof that changing a customer's contract will cause them to remain.

The selected churn model identifies customers who need retention attention while the GenAI advisory layer is designed to keep explanations grounded in approved inputs and free from protected demographic/family attributes.

## KPI Snapshot

Populate these values from the executed outputs in `notebooks/01_analysis.ipynb`:

| Measure | Result |
|---|---:|
| Total customers | 7,043 |
| Overall churn rate | 26.54% |
| Month-to-month churn rate | 42.71% |
| One-year contract churn rate | 11.27% |
| Two-year contract churn rate | 2.83%  | 
Tenure-churn correlation | 	-0.352 | 
Contract type is an observed association, not proof that contract length causes retention. Customers self-select into contract types based on commitment, satisfaction, pricing, and other circumstances. Retention actions should therefore use contract type as a predictive signal rather than assuming that moving customers to longer contracts will itself prevent churn.

## Model and Campaign Recommendation

The modelling pipeline cleans TotalCharges, applies preprocessing using the training data, compares Logistic Regression and Random Forest, and evaluates accuracy, recall, precision, F1, and ROC-AUC.

Random Forest was selected using 5-fold training cross-validation F1, rather than selecting the model from the test set.

| Measure | Random Forest |
|---|---:|
| Test accuracy | 76.15% |
| Test recall	| 71.12% |
| Test precision | 53.85% |
| Test F1|	61.29% |
| Test ROC-AUC	|0.832 |
| Train accuracy|	91.14% |
| Train-test accuracy gap	| 14.99 percentage points |

The 14.99 percentage-point train-test accuracy gap indicates a meaningful generalization risk and should be monitored before production deployment.

| Segment | Business profile | Customers | Avg. tenure | Avg. monthly charges | Avg. churn risk | Revenue at risk |
|---|---|---:|---:|---:|---:|---:|
| 0 | New, high-spend, high-risk | 2,111 | 13.6 mo | $79.14 | 76.40% | $127,734.69 |
| 1 | Established, high-spend, low-risk | 1,995 | 56.4 mo | $92.48 | 22.89% | $43,540.39 |
| 2 | New, low-spend, high-risk | 1,729 | 12.5 mo | $36.10 | 26.86% | $17,097.02 |
| 3 | Established, low-spend, low-risk | 1,208 | 54.1 mo | $34.89 | 6.65% | $3,352.68 |

Recommended target: Segment 0 - New, high-spend, high-risk
This segment combines high predicted churn risk with the largest expected monthly revenue at risk, making it the strongest starting point for a targeted retention campaign.

## Global Model Signals

The Random Forest's top three global feature-importance signals are:

Tenure — prioritize customers during their first 12 months for proactive retention check-ins and an annual-contract offer before renewal.
TotalCharges — prioritize high-value customers for tailored loyalty outreach and retention offers.
Month-to-month contract — offer eligible customers a time-limited annual-contract discount or fee waiver.

These are global predictive signals, not customer-specific causal explanations.

## Retention Advisory

The advisor retrieves one approved playbook clause before generating an explanation:

Clause 1: Risk probability at least 0.70: loyalty discount and a retention callback within 48 hours.
Clause 2: Risk probability from 0.40 to below 0.70: targeted email with an underused-service or upgrade offer.
Clause 3: Tenure below three months: route to onboarding, regardless of risk tier.
Clause 4: Explanations must not state or imply that protected demographics contributed to risk.
Retrieval is mandatory. Without the playbook, an LLM may guess a clause or invent an explanation. In this setting, that can cause the wrong customer action, create compliance exposure, and damage the audit trail.

## Governance Evidence

The GenAI advisory layer is designed to enforce Clause 4 through controlled inputs and output validation.

1. The LLM receives only the risk probability, tenure, retrieved clause, and top three global feature-importance signal names.
2. Customer IDs, raw demographic values, and full customer rows are not passed to the LLM.
3. The prompt explicitly prohibits demographic/family attributes from being used as explanations or retention reasons.
4. Generated text is checked for prohibited demographic references before it is accepted when an approved LLM provider is available.
5. The retrieved clause, permitted inputs, generated response, and validation result can be retained as an audit record.
The compliance claim for production should be supported by logs showing the input-field allowlist, retrieved clause, validator result, and any rejected output.

## Monitoring and Cost Control

Primary monitoring signal: Track the difference between predicted and observed churn rates by segment each month. Investigate potential model drift and consider retraining when the gap exceeds an agreed threshold, such as five percentage points, or when recall declines materially.

Cost control: Cache the approved playbook retrieval by risk tier and use the LLM only for the short, governance-safe explanation. Batch eligible requests and use an approved lower-cost model for simple standardized cases where appropriate.

Task 6 Execution Status

The deterministic retrieval logic has been completed and identifies Clause 3 for the selected test customer because the customer's tenure is below three months, even though the predicted churn probability is approximately 99.22%.

The actual grounded and ungrounded LLM calls remain pending assignment-approved LLM access. No LLM response has been fabricated.
## Required Completion Checklist

- [ ] Execute the grounded LLM call using an assignment-approved provider.
- [ ] Execute the ungrounded comparison call using the same approved provider.
- [ ] Record the exact LLM responses and validator result.
- [ ] Perform final memo review after Task 6 execution.
## Source Files

- [Notebook analysis](../notebooks/01_analysis.ipynb)
- [Data processing](../src/data_processing.py)
- [Retention advisor and validator](../src/retention_rag.py)
- [Detailed findings worksheet](ANALYSIS_NOTES.md)
