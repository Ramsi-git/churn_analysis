# Churn Analysis: Technical Notes & Findings
## Complete Documentation for Memo & Board Presentation

---

## PART 1: BUSINESS FRAMING & EXPLORATORY ANALYSIS

### Overall Churn Rate (KPI)
**Your number here:** _____ %

Record from notebook output:
```
Total Customers: [number]
Churned Customers: [number]
Retained Customers: [number]
Overall Churn Rate: [percentage]%
```

### Churn Rate by Contract Type
**Record your own numbers:**

| Contract Type | Churn Rate | Count | Churned |
|---|---|---|---|
| Month-to-month | ___% | ___ | ___ |
| One year | ___% | ___ | ___ |
| Two year | ___% | ___ | ___ |

### Churn Rate by Internet Service Type
**Record your own numbers:**

| Service Type | Churn Rate | Count |
|---|---|---|
| ___ | ___% | ___ |
| ___ | ___% | ___ |
| ___ | ___% | ___ |

### Analytical Question: Contract Correlation vs. Causation

**Your answer in one paragraph:**

[Your paragraph here - explain why month-to-month churn is high due to self-selection, not causation]

Key points to cover:
- Selection bias: Who self-selects into month-to-month vs. annual?
- Causation fallacy: Why forcing annual contracts won't replicate the effect
- Underlying drivers: What the real retention levers are

---

## PART 2: PREDICTIVE MODELLING

### TotalCharges Fix

**What was broken:**
- TotalCharges stored as string with blank values for new customers

**How you fixed it:**
- Identified [number] rows with missing TotalCharges
- These were customers with very low tenure
- Calculated: TotalCharges = tenure_months * MonthlyCharges

**Code location:** 
`notebooks/01_analysis.ipynb` → Cell "2.3 Fix TotalCharges"

---

### Model Performance Comparison

**Best model selected:** _______________

| Metric | Logistic Regression | Random Forest | Gradient Boosting |
|---|---|---|---|
| Train Accuracy | ___% | ___% | ___% |
| Test Accuracy | ___% | ___% | ___% |
| Test Recall | ___% | ___% | ___% |
| Test ROC-AUC | ____ | ____ | ____ |

**Why [best model] was chosen:**
- [Your reasoning]

### Analytical Question A: Accuracy vs. Recall

**Your churn rate (minority class):** ____%

**Naive baseline (always predict "No Churn"):**
- Accuracy: ____% ← Misleading!
- Recall: ____% ← Catches no churners

**Your best model:**
- Accuracy: ____% 
- Recall: ____% ← Catches ____% of actual churners

**Explanation for the CFO (1-2 paragraphs):**

[Write here why accuracy alone is misleading; what recall means in business terms]

Key insight: 
- High accuracy = large majority class dominates the metric
- Recall = percentage of actual churners your system identifies
- If recall is 60%, you miss 40% of people about to leave
- That's the real cost to the business

### Analytical Question B: Train vs. Test Accuracy

**Your numbers:**
- Training Accuracy: _____%
- Test Accuracy: _____%
- Overfitting Gap: _____%

**Gap Analysis:**

IF gap < 1%:
"Our model generalizes excellently. The near-identical accuracy on held-out test data indicates the retention predictions will reliably apply to future customers we haven't seen before. Safe to defend to the board."

IF gap 1-5%:
"Model shows acceptable generalization with [gap]% train-test gap. We recommend quarterly retraining as customer behavior evolves. Performance is defensible."

IF gap > 5%:
"Model shows signs of overfitting with [gap]% train-test gap. We should simplify the model (reduce features/depth) before deployment. Current predictions may not generalize to new customers."

**Your analysis:**

[Fill in your conclusion]

---

## PART 3: FEATURE IMPORTANCE & SEGMENTATION

### Top 3 Features

Rank each and write the specific action a retention manager could take:

**Feature 1:** _______________
- Importance score: ____
- **Specific action:** [Write a concrete retention tactic, not "improve satisfaction"]
  Example: "Offer customers with low MonthlyCommitment a bundle upgrade to 3-year contract"

**Feature 2:** _______________
- Importance score: ____
- **Specific action:** [Concrete tactic]

**Feature 3:** _______________
- Importance score: ____
- **Specific action:** [Concrete tactic]

---

### Customer Segments (K-Means Clustering)

**Number of clusters:** ___ (3 or 4)

**Segment profiles:**

| Segment | Name | Count | Avg Tenure (mo) | Avg Spend ($/mo) | Churn Risk | Revenue at Risk |
|---|---|---|---|---|---|---|
| 0 | ___ | ___ | ___ | ___ | ___% | $___ |
| 1 | ___ | ___ | ___ | ___ | ___% | $___ |
| 2 | ___ | ___ | ___ | ___ | ___% | $___ |
| [3] | ___ | ___ | ___ | ___ | ___% | $___ |

### Analytical Question: Which Segment to Target First?

**Your recommendation:** Segment [#] - **[Name]**

**Business case (1-2 paragraphs):**

[Explain your recommendation by weighing:]
- Revenue at risk (potential impact if saved)
- Segment size (population to reach)
- Churn risk (urgency)
- Cost-benefit of campaign

Example calculation: 
"Segment 1 (High-spend new customers) has 800 customers at $85/month with 45% churn risk. If we save even 20% of them, we preserve $163k in annual revenue. This is the highest ROI per dollar spent on retention."

---

## PART 4: GenAI ADVISORY LAYER & GOVERNANCE

### Retention Playbook (Exact Text)

```
Clause 1 — High Risk (probability ≥ 0.70): Offer a loyalty discount and a callback 
from a retention specialist within 48 hours.

Clause 2 — Moderate Risk (0.40–0.70): Send a targeted email highlighting an underused 
service or a contract upgrade offer.

Clause 3 — New Customer, Any Risk, Tenure < 3 months: Route to the onboarding team 
instead of the standard retention flow.

Clause 4 — Non-Discrimination Rule: Retention explanations must never state or imply 
that gender, senior-citizen status, or family/partner status contributed to a customer's risk 
score, even where a statistical correlation exists in the data.
```

### Test Customer (High-Risk)

**Customer ID:** _______________
- Tenure: ___ months
- Monthly Charges: $___
- Total Charges: $___
- Churn Risk: ____%
- Internet Service: ___
- Contract: ___

**Top 3 Risk Factors (from feature importance):**
1. _______________
2. _______________
3. _______________

**Applicable Clause (from retrieval logic):**
Clause [#] - [Tier]

---

### Analytical Question A: Hallucination Without Retrieval

**Test setup:**
- Called LLM WITHOUT providing the playbook text
- Asked: "Which clause applies? (Clause 1, 2, 3, or 4)"
- LLM had no grounding in official clauses

**What the LLM said:**
```
[Paste exact LLM response here]
```

**Expected answer:** Clause [#]
**LLM gave:** Clause [#] or [Hallucination]
**Correct?** Yes / No

**Failure mode name:** CONTEXT COLLAPSE / CONFABULATION

**Why this is worse in retention/compliance than casual chatbot:**

[Write 2-3 paragraphs covering:]
- Business risk: Wrong clause = wrong retention action
- Compliance risk: Hallucination might violate Clause 4
- Trust damage: System deemed unreliable
- High stakes: Unlike casual Q&A, this affects real customers

Example: "If the LLM hallucinated and mentioned 'female senior citizen' in explaining churn, we'd be in legal risk. Audit would find our system violated its own governance rule. This is not a 'oops' moment; it's a compliance failure."

---

### Analytical Question B: Data Leakage Prevention

**Scenario:**
You could have passed the customer's FULL data row into the LLM:
```
{
  'customerID': '1234',
  'tenure': 12,
  'gender': 'Female',           ← PROBLEM
  'SeniorCitizen': 1,           ← PROBLEM
  'Partner': 'No',              ← PROBLEM
  'Dependents': 'Yes',          ← PROBLEM
  'churn_probability': 0.78,
  ...
}
```

**What could go wrong:**

[Write 2-3 paragraphs covering:]
- Direct leakage: LLM sees demographics and uses them
- Implicit leakage: LLM infers demographic patterns even if told not to use them
- Prompt injection: Attacker alters prompt to ask for demographic explanations
- Audit failure: Explanation correlates with demographics; you can't defend it

**What you actually did:**

You passed ONLY:
```
{
  'customer_id': '1234',
  'risk_probability': 0.78,
  'tenure': 12,
  'top_features': ['Feature1', 'Feature2', 'Feature3'],  ← Names only, not values
  'clause': 'Clause 1 - High Risk'
}
```

**How this prevents leakage:**

[Write 1 paragraph]
- Demographics never entered the LLM context
- Even if adversary tries, the data isn't there
- Code is audit-ready
- Compliance test: Pass ✓

---

## PART 5: EXECUTIVE MEMO

### One-Page Memo (Required Deliverable)

**From:** [Your name], Data Science Team  
**To:** Board & CFO  
**Date:** [Today's date]  
**Subject:** Customer Churn Analysis: Predictive Model & Retention Strategy  

---

#### HEADLINE (One sentence CFO can repeat)

[Write your headline here]

Example: "Our churn model identifies 73% of at-risk customers and recommends targeted interventions that could preserve $2.1M in annual revenue."

#### Churn KPI & Baseline

[Fill in your overall churn rate and key breakdowns]

#### Recommended Segment for Retention Campaign

**Target:** Segment [#] - [Name]

**Trade-off analysis:** [1-2 sentences weighing churn risk vs. revenue impact]

Example: "While Segment 2 has the highest churn risk (48%), Segment 1 has lower risk (32%) but 3x the monthly spend ($85 vs. $28). We recommend Segment 1 first because saving 100 high-value customers nets more revenue than saving 300 budget customers at equal risk."

#### Monitoring Signal (Post-Launch)

[Name ONE concrete metric you would track to detect model decay]

NOT: "Check accuracy periodically"  
YES: "Track the gap between predicted churn rate and actual churn rate by segment, monthly. If gap widens > 5%, retrain the model with fresh data."

#### Governance: Non-Discrimination Proof

[One sentence describing how you would prove Clause 4 enforcement from logs]

Example: "All generated explanations are validated against a compliance checker that flags demographic keywords; logs show 0 violations across 100% of explanations generated."

#### Cost Control for High-Volume LLM Calls

[One specific design change to reduce API cost without breaking citation guarantee]

Example: "Cache the playbook clause retrieval (same for all high-risk tiers); only call LLM with the specific customer's top features. This reduces tokens per call by 60%."

---

### Extended Notes for Board Q&A

#### TotalCharges Fix (Your own words)

Explain:
- How you identified the problem
- Why it mattered (for train-test validity)
- How you fixed it
- Why your fix is defensible

[Write 1-2 paragraphs]

#### Train vs. Test Accuracy Trade-Off

Explain:
- Your gap percentage
- What it means for generalization
- Whether you'd defend this model to the board as-is, or simplify first
- Why that increases/decreases confidence

[Write 1-2 paragraphs]

#### What Happened When You Skipped Retrieval

Explain:
- The hallucination example from your test
- Why it's worse than a casual chatbot failure
- How it could have exposed the company to compliance risk
- Why retrieval is mandatory, not optional

[Write 2-3 paragraphs]

#### Exactly What Was Passed to the LLM (Code Reference)

Show:
- The exact fields/values you passed
- Where in the notebook demographic columns were excluded
- Why this prevents both direct and implicit leakage

Example code snippet + explanation:
```python
user_message = f"""
Customer ID: {customer_id}
Churn Risk: {churn_probability:.2%}
Tenure: {tenure} months
Top 3 Features: {feature_1}, {feature_2}, {feature_3}  ← NAMES only, not values
Applicable Clause: {clause_text}
"""
# Demographic columns DELIBERATELY EXCLUDED
# This ensures audit trail is clean
```

[Write 1 paragraph explanation]

---

## APPENDIX: Code Locations

| Finding | Notebook Cell | File |
|---|---|---|
| Overall churn rate | 1.2 | 01_analysis.ipynb |
| Churn by contract | 1.3 | 01_analysis.ipynb |
| TotalCharges fix | 2.3 | 01_analysis.ipynb |
| Feature importance | 4.1 | 01_analysis.ipynb |
| Segmentation | 5.1-5.5 | 01_analysis.ipynb |
| Retrieval logic | 6.3 | 01_analysis.ipynb |
| Governance validator | 6.3 | src/retention_rag.py |
| LLM with retrieval | 6.5 | 01_analysis.ipynb |
| Hallucination test | 6.6 | 01_analysis.ipynb |

---

**Ready to convert to Word document and add to GitHub.**
