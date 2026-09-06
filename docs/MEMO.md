# Customer Churn Analysis: Executive Memo

**From:** Data Science Team  
**To:** Board and CFO  
**Date:** September 6, 2026  
**Subject:** Predictive churn model and retention strategy

## Executive Summary

The analysis combines exploratory analysis, churn prediction, customer segmentation, and a governance-controlled retention advisor. The model is designed to prioritize customers for retention outreach; it is not a causal model and should not be used to force customers into longer contracts.

**Headline:** The selected churn model identifies customers who need retention attention while excluding protected demographic attributes from model features and LLM context.

## KPI Snapshot

Populate these values from the executed outputs in `notebooks/01_analysis.ipynb`:

| Measure | Result |
|---|---:|
| Total customers | `[run notebook]` |
| Overall churn rate | `[run notebook]` |
| Month-to-month churn rate | `[run notebook]` |
| One-year contract churn rate | `[run notebook]` |
| Two-year contract churn rate | `[run notebook]` |

Contract type is an observed association, not proof that contract length causes retention. Customers self-select into contracts based on commitment, satisfaction, and circumstances. Retention action should therefore focus on service experience, tenure, pricing, and engagement signals rather than simply moving customers to annual contracts.

## Model and Campaign Recommendation

The pipeline cleans `TotalCharges`, encodes permitted service and contract variables, excludes `gender`, `SeniorCitizen`, `Partner`, and `Dependents`, and compares logistic regression, random forest, and gradient boosting. The best model is selected by test ROC-AUC, with recall treated as a critical operational metric because missed churners represent lost intervention opportunities.

| Measure | Result |
|---|---:|
| Selected model | `[run notebook]` |
| Test accuracy | `[run notebook]` |
| Test recall | `[run notebook]` |
| Test ROC-AUC | `[run notebook]` |
| Train-test accuracy gap | `[run notebook]` |

The first retention campaign should target the segment with the strongest combination of churn risk, population size, and revenue at risk. Complete the segment table from the notebook before launch:

| Segment | Business profile | Customers | Avg. churn risk | Revenue at risk |
|---:|---|---:|---:|---:|
| 0 | `[run notebook]` | `[run notebook]` | `[run notebook]` | `[run notebook]` |
| 1 | `[run notebook]` | `[run notebook]` | `[run notebook]` | `[run notebook]` |
| 2 | `[run notebook]` | `[run notebook]` | `[run notebook]` | `[run notebook]` |

**Recommended target:** Segment `[run notebook]`, because it offers the best expected retention value after balancing risk, reachable volume, and customer value.

## Retention Advisory

The advisor retrieves one approved playbook clause before generating an explanation:

- **Clause 1:** Risk probability at least 0.70: loyalty discount and a retention callback within 48 hours.
- **Clause 2:** Risk probability from 0.40 to below 0.70: targeted email with an underused-service or upgrade offer.
- **Clause 3:** Tenure below three months: route to onboarding, regardless of risk tier.
- **Clause 4:** Explanations must not state or imply that protected demographics contributed to risk.

Retrieval is mandatory. Without the playbook, an LLM may guess a clause or invent an explanation. In this setting, that can cause the wrong customer action, create compliance exposure, and damage the audit trail.

## Governance Evidence

The implementation enforces Clause 4 in code:

1. Protected columns are excluded before model training.
2. The LLM receives only customer ID, risk probability, tenure, top feature names, and the retrieved clause.
3. Raw demographic values and full customer rows are not passed to the LLM.
4. Generated text is checked for prohibited demographic references before it is accepted.
5. The retrieved clause and validation result can be retained as an audit record.

The compliance claim for production should be supported by logs showing the input-field allowlist, retrieved clause, validator result, and any rejected output.

## Monitoring and Cost Control

**Primary monitoring signal:** Track the difference between predicted and observed churn rates by segment each month. Investigate and retrain when the gap exceeds the agreed threshold, such as five percentage points, or when recall declines materially.

**Cost control:** Cache the approved playbook retrieval by risk tier and use the LLM only for the short, governance-safe explanation. Batch eligible requests and reserve the more capable model for cases that need escalation.

## Required Completion Checklist

- [ ] Run all notebook cells and copy the actual KPI values into this memo.
- [ ] Record model accuracy, recall, ROC-AUC, and train-test gap.
- [ ] Copy the segment profiles and select the campaign target.
- [ ] Record the test customer's retrieved clause and risk factors.
- [ ] Save the generated explanation and validator result for the audit trail.
- [ ] Review the completed memo for unsupported causal claims before distribution.

## Source Files

- [Notebook analysis](../notebooks/01_analysis.ipynb)
- [Data processing](../src/data_processing.py)
- [Retention advisor and validator](../src/retention_rag.py)
- [Detailed findings worksheet](ANALYSIS_NOTES.md)
