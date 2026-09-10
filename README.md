# Telecom Customer Churn Analysis & AI-Driven Retention Strategy

A complete end-to-end data science project analyzing customer churn, building predictive models, and implementing a governance-aware GenAI advisory layer for the retention team.

## 📋 Project Structure

```
churn_analysis/
├── notebooks/
│   └── 01_analysis.ipynb          # Main analysis notebook (all 4 parts)
├── src/
│   ├── data_processing.py         # Data loading, cleaning, preprocessing
│   └── retention_rag.py           # RAG module, playbook, governance validator
├── data/
│   └── [Dataset downloaded at runtime]
├── docs/
│   ├── [Analysis charts and visualizations]
│   └── MEMO.md                    # Executive memo
├── requirements.txt               # Python dependencies
└── README.md                       # This file
```

## 🎯 Project Overview

### Part 1: Business Framing & Exploratory Analysis
- Load and explore 7,043 customer records from IBM's Telco dataset
- Compute overall churn rate and break down by Contract type and Internet Service
- Analyze tenure-churn correlation
- **Key insight**: Contract type is correlation, not causation (self-selection bias)

### Part 2: Predictive Modelling & Business Segmentation
- Clean data: Fix inconsistent `TotalCharges` column, handle missing values
-  **Governance Rule**: Protected demographic/family variables (gender, SeniorCitizen, Partner, Dependents) are retained for model auditing but are not used as causal explanations or retention reasons.
- Train and compare: Logistic Regression (baseline), Random Forest
- Evaluate with accuracy, recall, precision, and ROC-AUC
- Identify overfitting: Compare train vs. test accuracy
- Extract feature importance for actionable insights
- Segment customers into 3-4 clusters based on tenure, spend, and churn risk

### Part 3: GenAI Advisory Layer — Prompt Engineering & RAG
- Build **retrieval-augmented generation (RAG)** advisor without vector DB
- Implement exact retention playbook (4 clauses) with rule-based retrieval
- **Clause 1** (High Risk ≥70%): Loyalty discount + 48-hour callback
- **Clause 2** (Moderate Risk 40-70%): Targeted email + upgrade offer
- **Clause 3** (New Customer <3 months): Route to onboarding team
- **Clause 4** (Non-Discrimination): Never mention demographics
- Prepare an LLM prompt using the retrieved clause, risk probability, tenure, and top 3 global feature-importance signals
- Include an ungrounded comparison call to evaluate clause selection without playbook retrieval
- Validate the LLM output for compliance when an approved LLM provider is available

### Part 4: Governance, Monitoring, Cost & Board Memo
- Executive one-page memo (no code, CFO-ready language)
- Document key decisions and trade-offs
- Recommend segment for retention campaign
- Propose monitoring signal for model retraining
- Outline governance proof for audit (non-discrimination enforcement)
- Suggest cost control for high-volume LLM calls

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-key-here"

# Or add to .env file (install python-dotenv)
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 3. Run the Analysis
Open `notebooks/01_analysis.ipynb` in Jupyter and run cells in order.

The notebook will:
- Download data from GitHub
- Execute all 4 parts
- Save visualizations to `docs/`
- Generate text outputs for memo

## 📊 Key Findings (Your Numbers)

### Part 1: KPI & Correlation
-  Overall churn rate: 26.54%
- Month-to-month churn: 42.71%
- 1-year contract churn: 11.27%
- 2-year contract churn: 2.83%

### Part 2: Model Performance
-  Best model: Random Forest
- Test set accuracy: 76.15%
- Test set recall: 71.12% (critical for identifying churners)
- Train vs. test accuracy gap: 14.99 percentage points (indicates overfitting/generalization risk)
- Test set ROC-AUC: 0.832

### Part 3: Feature Importance

Top 3 global model feature-importance signals:

1. Tenure → Prioritize customers in their first 12 months for proactive retention check-ins and an annual-contract offer before renewal.
2. TotalCharges → Prioritize high-value customers for tailored loyalty outreach and retention offers.
3. Month-to-month contract → Offer eligible month-to-month customers a time-limited annual-contract discount or fee waiver.

Note: These are predictive signals from the Random Forest, not proof of causal effects.

### Part 4: Customer Segments

* New, high-spend, high-risk - 2,111 customers, $127,734.69 expected monthly revenue at risk
* Established, high-spend, low-risk - 1,995 customers, $43,540.39 expected monthly revenue at risk
* New, low-spend, high-risk - 1,729 customers, $17,097.02 expected monthly revenue at risk
* Established, low-spend, low-risk - 1,208 customers, $3,352.68 expected monthly revenue at risk

Recommended for first retention campaign: New, high-spend, high-risk. This segment combines a 76.40% average predicted churn risk with $79.14 average monthly charges and approximately $127,734.69 in expected monthly revenue at risk.


## 🔒 Governance & Compliance

### Non-Discrimination (Clause 4)
- ✓  Protected demographic/family variables are not used in LLM explanations or retention recommendations
- ✓ LLM receives only: risk_probability, tenure_months, top_3_feature_names
- ✓ LLM prompted to forbid demographic mentions
- ✓ Validator checks LLM output for compliance

### Audit Trail
The planned customer explanation includes:
- Risk probability (numeric, defensible)
- Top 3 business drivers (service/contract/engagement, not demographics)
- Retrieved clause (approved, standardized text)
- LLM explanation (grounded in above, validated)

### Monitoring Signal
After deployment, track: **Difference between predicted churn rate and actual churn rate by segment, monthly**, along with the model's recall and ROC-AUC on newly labeled outcomes.

### Cost Control
For high-volume LLM explanations:
- **Design change**: Cache retrieved clauses (same for all high-risk customers)
- Batch requests where possible
- Use an approved lower-cost LLM for simple, standardized clauses where appropriate
- Monitor token usage per segment

## 📝 Files in This Project

| File | Purpose |
|------|---------|
| `notebooks/01_analysis.ipynb` | Complete Jupyter notebook with all 4 parts |
| `src/data_processing.py` | DataProcessing class: load, clean, preprocess data |
| `src/retention_rag.py` | Playbook, Retriever, Validator, Advisor classes |
| `docs/MEMO.md` | One-page executive memo (required deliverable) |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Ignore data files and secrets |

## 🔧 Optional: Bonus Streamlit App

To build the optional bonus app (Task 6 wrapper in Streamlit):

```bash
pip install streamlit

# Create app file
cat > streamlit_app.py << 'EOF'
import streamlit as st
# [See bonus section in notebook or notes doc]
EOF

streamlit run streamlit_app.py
```

## 📖 Documentation

- **MEMO.md**: Executive one-pager with headline KPI, segment recommendation, monitoring plan, governance statement, cost strategy
- **Notebook cells**: Each part includes "Analytical Questions" with detailed answers
- **Code comments**: Governance decisions flagged with explicit reasoning

## ⚠️ Important Notes

1. **Data Privacy**: The dataset is real IBM Telco data. All analysis is academic/demonstration.
2. **LLM Calls**: Requires OpenAI API key. Estimated cost: ~$0.10-0.50 for full analysis.
3. **Generalization**: Train-test split is 80/20. Monitor accuracy gap for overfitting.
4. **Non-Discrimination**: Protected demographic/family variables are not used as causal explanations or retention reasons. The LLM prompt and output validation prevent demographic attributes from being used in retention explanations.

## 🎓 Learning Outcomes

After completing this project, you will understand:
- End-to-end ML pipeline: EDA → Modeling → Deployment
- How to handle minority class imbalance (high recall = catch churners)
- RAG without vector DB (simple rule-based retrieval is often sufficient)
- Governance in practice (demographic exclusion, output validation)
- How to communicate data science to executives (metrics, trade-offs, risks)

## 📞 Questions?

Refer to the "Analytical Questions" sections in the notebook for in-depth answers:
- **Part 1**: Why is contract type correlation, not causation?
- **Part 2A**: Why accuracy alone is misleading for minority classes
- **Part 2B**: How to diagnose overfitting
- **Part 3A**: What hallucination looks like and why it's worse in compliance contexts
- **Part 3B**: How demographic data leakage happens and how to prevent it

---

**Last Updated**: Sept 6, 2026  
**Status**: Analysis and modelling completed; GenAI advisory execution pending approved LLM access and final executive memo validation.
