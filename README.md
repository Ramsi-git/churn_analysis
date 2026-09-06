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
- **Governance Rule**: Exclude protected demographic columns (gender, SeniorCitizen, Partner, Dependents) from model features
- Train and compare: Logistic Regression (baseline), Random Forest, Gradient Boosting
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
- Call LLM with retrieved clause + top 3 features (governance-safe)
- Demonstrate hallucination without retrieval
- Validate LLM output for compliance

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
- Overall churn rate: **[Fill in after running]**%
- Month-to-month churn: **[Fill in]**%
- 1-year contract churn: **[Fill in]**%
- Correlation insight: Self-selection bias (committed customers chose commitment)

### Part 2: Model Performance
- Best model: **[Logistic Regression / Random Forest / Gradient Boosting]**
- Test set accuracy: **[Fill in]**%
- Test set recall: **[Fill in]**% (critical for identifying churners)
- Train vs. test gap: **[Fill in]**% (indicates generalization)

### Part 3: Feature Importance
Top 3 features driving churn:
1. **[Feature name]** → **Action**: [Specific retention tactic]
2. **[Feature name]** → **Action**: [Specific retention tactic]
3. **[Feature name]** → **Action**: [Specific retention tactic]

### Part 4: Customer Segments
- Segment 0: **[Name]** - [Count] customers, $[Revenue at risk]
- Segment 1: **[Name]** - [Count] customers, $[Revenue at risk]
- Segment 2: **[Name]** - [Count] customers, $[Revenue at risk]

**Recommended for first retention campaign**: Segment [#] - **[Name]**
(Balances high risk with sufficient volume and revenue impact)

## 🔒 Governance & Compliance

### Non-Discrimination (Clause 4)
- ✓ Demographic columns excluded from model training
- ✓ LLM receives only: risk_probability, tenure_months, top_3_feature_names
- ✓ LLM prompted to forbid demographic mentions
- ✓ Validator checks LLM output for compliance

### Audit Trail
Every customer explanation includes:
- Risk probability (numeric, defensible)
- Top 3 business drivers (service/contract/engagement, not demographics)
- Retrieved clause (approved, standardized text)
- LLM explanation (grounded in above, validated)

### Monitoring Signal
After deployment, track: **[Your monitoring metric here]**
Example: "Difference between predicted churn rate and actual churn rate by segment, monthly"

### Cost Control
For high-volume LLM explanations:
- **Design change**: Cache retrieved clauses (same for all high-risk customers)
- Batch requests where possible
- Use cheaper model (GPT-3.5 instead of GPT-4) for simple clauses
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
4. **Non-Discrimination**: Demographic exclusion is MANDATORY, not optional. Code enforces this.

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
**Status**: Ready for analysis
