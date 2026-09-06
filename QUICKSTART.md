# Quick Start Guide - Customer Churn Analysis

## 🎯 Start Here

### Step 1: Install Python Dependencies
```powershell
cd C:\Users\hp\Desktop\churn_analysis
pip install -r requirements.txt
```

### Step 2: Set OpenAI API Key (Required for Part 3)
```powershell
# Option A: Set environment variable (temporary for this session)
$env:OPENAI_API_KEY = "sk-your-key-here"

# Option B: Create .env file (persistent)
# Add to .env:
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Open Jupyter Notebook
```powershell
jupyter notebook notebooks/01_analysis.ipynb
```

### Step 4: Run All Cells
Click "Cell" → "Run All" or press Ctrl+A then Ctrl+Enter

---

## 📚 What You'll Get

After running the notebook, you'll have:

- **Visualizations** in `docs/`:
  - `01_churn_by_contract.png`
  - `02_churn_by_internet.png`
  - `03_tenure_analysis.png`
  - `04_feature_importance.png`

- **Data** in your notebook:
  - Overall churn rate (KPI)
  - Model performance metrics
  - Feature importance scores
  - Customer segments with names and profiles
  - LLM-generated retention explanations

- **Notes** for the executive memo in `docs/ANALYSIS_NOTES.md`

---

## ✍️ After Running: Complete the Documentation

1. Open `docs/ANALYSIS_NOTES.md`
2. Fill in your numbers from the notebook outputs
3. Write the analytical questions in your own words
4. Copy the verified findings into `docs/MEMO.md`
5. Review the memo for unsupported causal claims before sharing

---

## 🤖 Project Modules

### `src/data_processing.py`
```python
from src.data_processing import ChurnDataProcessor

processor = ChurnDataProcessor()
df = processor.load_data('https://...')
X, y, X_full, df_clean = processor.preprocess(df)
X_train, X_test, y_train, y_test = processor.split_and_scale(X, y)
```

### `src/retention_rag.py`
```python
from src.retention_rag import RetentionAdvisor

advisor = RetentionAdvisor()
context, clause = advisor.prepare_llm_context(
    customer_id, churn_risk, tenure, top_3_features
)
# Then call LLM with context (see notebook for example)
```

---

## 🔑 Key Learnings

- **Part 1**: Churn ≠ just contract type; self-selection bias matters
- **Part 2**: Recall >> Accuracy for minority classes; watch for overfitting
- **Part 3**: Retrieval prevents hallucination; data governance is non-negotiable
- **Part 4**: Governance proof + monitoring plan = board-ready system

---

## 💡 Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'openai'"
- **Fix**: `pip install openai`

**Issue**: "OPENAI_API_KEY not set"
- **Fix**: Set environment variable before running LLM cells (Part 3)

**Issue**: "Data download failed"
- **Fix**: Check internet connection; notebook downloads from GitHub at runtime

**Issue**: "Notebook takes too long"
- **Fix**: This is normal for Model training. Random Forest/Gradient Boosting may take 30-60 seconds.

---

## 📞 Questions?

- **Q: Do I need a vector database?**  
  A: No! The notebook uses simple rule-based retrieval (if tenure < 3 OR risk >= 0.70, etc.)

- **Q: Why exclude demographic columns?**  
  A: Governance requirement (Clause 4). Prevents bias and ensures audit-ready system.

- **Q: Can I skip Part 3 (LLM)?**  
  A: Part 3 is required per assignment. You can test without OpenAI key, but memo requires LLM explanation.

- **Q: How do I make a Word document from the notes?**  
  A: Open `docs/ANALYSIS_NOTES.md`, copy content, paste into Word, format, save as .docx

---

**Project Location**: `C:\Users\hp\Desktop\churn_analysis`  
**Status**: Ready to run  
**Last Updated**: Sept 6, 2026  
