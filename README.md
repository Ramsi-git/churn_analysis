# Telecom Customer Churn Analysis & AI-Driven Retention Strategy

An end-to-end data science project analyzing telecom customer churn, building predictive models, segmenting customers by retention risk, and designing a governance-aware GenAI advisory layer for retention teams.

## 📋 Project Structure
 
```text
churn_analysis/
├── notebooks/
│   └── 01_analysis.ipynb          # Main analysis notebook
├── src/
│   ├── data_processing.py         # Data loading, cleaning, preprocessing
│   └── retention_rag.py           # Retention playbook, retrieval, validation
├── data/
│   └── [Dataset downloaded at runtime]
├── docs/
│   ├── ANALYSIS_NOTES.md          # Detailed analysis and decisions
│   └── MEMO.md                    # Executive memo
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## 🎯 Project Overview

This project uses the IBM Telco Customer Churn dataset to analyze customer churn, develop a churn prediction model, identify high-value/high-risk customer segments, and design a governance-aware retention advisory workflow.

### Task 1: Business Framing & Exploratory Analysis

* Analyze 7,043 telecom customer records.
* Calculate the overall churn rate.
* Compare churn across Contract types and Internet Service categories.
* Analyze the relationship between tenure and churn.
* Treat observed relationships as correlations rather than causal effects because customer contract choices may involve self-selection.

### Task 2: Data Preparation & Predictive Modelling

* Clean the `TotalCharges` column.
* Handle the 11 blank `TotalCharges` values associated with zero-tenure customers.
* Remove `customerID` from modelling features.
* Separate the target variable `Churn`.
* Encode categorical variables using one-hot encoding.
* Standardize numerical variables.
* Fit preprocessing on the training data and transform the test data separately to avoid data leakage.
* Compare Logistic Regression as a baseline with Random Forest.
* Evaluate models using accuracy, precision, recall, F1-score, and ROC-AUC.
* Compare training and test performance to identify generalization risk.
* Select the Random Forest model using 5-fold training cross-validation F1-score.

### Task 3: Feature Importance & Customer Segmentation

* Extract global Random Forest feature-importance signals.
* Identify the top three predictive signals for business action.
* Segment customers into four groups using tenure, MonthlyCharges, and predicted churn probability.
* Estimate expected monthly revenue at risk for each segment.
* Prioritize the segment with the greatest combination of churn risk and revenue exposure.

### Task 4: Governance-Aware GenAI Advisory Layer

* Implement a rule-based retention playbook with four approved clauses.
* Retrieve the applicable clause using risk probability and tenure.
* Give Clause 3 priority when tenure is below three months.
* Prepare a constrained LLM prompt using only approved information.
* Prevent demographic attributes from being used as retention explanations.
* Validate generated responses for governance compliance when an assignment-approved LLM provider is available.
* Compare the grounded workflow with an ungrounded clause-selection call.

### Task 5: Monitoring, Cost Control & Executive Communication

* Prepare an executive-facing retention recommendation.
* Define a model monitoring signal for future retraining decisions.
* Document governance and audit controls.
* Recommend cost-control measures for high-volume LLM usage.
* Communicate technical results in business-oriented language.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure an Assignment-Approved LLM Provider

Task 6 requires an assignment-approved generative LLM provider.

Configure the approved provider securely through an environment variable or approved local runtime. Never hard-code or commit API credentials to the repository.

If an approved LLM provider is not available, the following components can still be reviewed and evaluated:

* Data cleaning
* Exploratory analysis
* Predictive modelling
* Feature importance
* Customer segmentation
* Rule-based retrieval
* Prompt design
* Governance controls

The actual grounded and ungrounded LLM executions remain pending until approved LLM access is available.

### 3. Run the Analysis

Open:

```text
notebooks/01_analysis.ipynb
```

and run the notebook cells in order.

The notebook performs the analysis, modelling, segmentation, feature-importance analysis, and retention-advisory preparation.

## 📊 Key Findings

### Business KPIs

| Metric                        | Result |
| ----------------------------- | -----: |
| Overall churn rate            | 26.54% |
| Month-to-month contract churn | 42.71% |
| One-year contract churn       | 11.27% |
| Two-year contract churn       |  2.83% |
| Tenure-churn correlation      | -0.352 |

The contract-level churn differences are treated as correlations rather than proof that contract type itself causes churn.

### Model Performance

The Random Forest was selected using 5-fold training cross-validation F1-score.

| Metric                  |           Random Forest |
| ----------------------- | ----------------------: |
| Test accuracy           |                  76.15% |
| Test precision          |                  53.85% |
| Test recall             |                  71.12% |
| Test F1-score           |                  61.29% |
| Test ROC-AUC            |                   0.832 |
| Train accuracy          |                  91.14% |
| Train-test accuracy gap | 14.99 percentage points |

The 14.99 percentage-point training/test accuracy gap indicates a generalization risk that should be monitored after deployment.

For comparison, Logistic Regression achieved 80.62% test accuracy, 60.61% F1-score, and 0.842 ROC-AUC. The Random Forest was selected because model selection was based on training cross-validation F1-score rather than test-set ROC-AUC alone.

## 🔎 Top 3 Global Model Feature-Importance Signals

The following are **global predictive signals from the Random Forest**, not customer-specific causal explanations.

1. **Tenure**
   Prioritize customers during their first 12 months for proactive retention check-ins and an annual-contract offer before renewal.

2. **TotalCharges**
   Prioritize high-value customers for tailored loyalty outreach and retention offers.

3. **Month-to-month contract**
   Offer eligible month-to-month customers a time-limited annual-contract discount or fee waiver.

These feature-importance signals indicate predictive relevance in the trained model. They should not be interpreted as proof that changing a feature will directly cause churn to decrease.

## 👥 Customer Segmentation

Four customer segments were created using:

* Tenure
* MonthlyCharges
* Predicted churn probability

| Segment                           | Customers | Avg. Tenure | Avg. Monthly Charges | Avg. Churn Risk | Expected Monthly Revenue at Risk |
| --------------------------------- | --------: | ----------: | -------------------: | --------------: | -------------------------------: |
| New, high-spend, high-risk        |     2,111 | 13.6 months |               $79.14 |          76.40% |                      $127,734.69 |
| Established, high-spend, low-risk |     1,995 | 56.4 months |               $92.48 |          22.89% |                       $43,540.39 |
| New, low-spend, high-risk         |     1,729 | 12.5 months |               $36.10 |          26.86% |                       $17,097.02 |
| Established, low-spend, low-risk  |     1,208 | 54.1 months |               $34.89 |           6.65% |                        $3,352.68 |

### Recommended First Retention Campaign

**New, high-spend, high-risk customers** are the recommended first target.

This segment has:

* 2,111 customers
* 76.40% average predicted churn risk
* $79.14 average monthly charges
* Approximately $127,734.69 expected monthly revenue at risk

This provides the strongest combination of predicted churn exposure and potential revenue impact among the four segments.

## 🤖 Retention Advisory & RAG Logic

The retention advisory uses a simple rule-based retrieval approach rather than a vector database.

### Retention Playbook

**Clause 1 — High Risk (probability ≥ 0.70):**
Offer a loyalty discount and a callback from a retention specialist within 48 hours.

**Clause 2 — Moderate Risk (0.40–0.70):**
Send a targeted email highlighting an underused service or a contract upgrade offer.

**Clause 3 — New Customer, Any Risk, Tenure < 3 months:**
Route to the onboarding team instead of the standard retention flow.

**Clause 4 — Non-Discrimination Rule:**
Retention explanations must never state or imply that gender, senior-citizen status, or family/partner status contributed to a customer's risk score, even where a statistical correlation exists in the data.

### Retrieval Priority

If a customer's tenure is below three months, **Clause 3 takes priority**, regardless of the customer's predicted churn probability.

For the flagged customer used in Task 6:

* Predicted churn risk: approximately **99.22%**
* Tenure: **1 month**
* Expected clause: **Clause 3**

The deterministic retrieval result is therefore:

> Route the customer to the onboarding team instead of the standard retention flow.

## 🔒 Governance & Compliance

### Non-Discrimination Controls

The retention advisory is designed to prevent demographic attributes from becoming retention explanations or recommendations.

The LLM input is restricted to:

* `risk_probability`
* `tenure_months`
* Retrieved retention clause
* Top three global feature-importance names

The LLM is **not provided with**:

* `customerID`
* The customer's full dataset row
* Raw demographic attributes
* Gender
* SeniorCitizen
* Partner
* Dependents

The system prompt also prohibits the model from stating or implying that protected demographic/family attributes contributed to the customer's risk.

### Output Validation

Generated responses should be validated before being used by a retention team.

The validation layer is designed to check that the response:

* Follows the retrieved playbook clause.
* Includes the required risk probability and tenure.
* Does not introduce unsupported customer facts.
* Does not mention prohibited demographic/family attributes.
* Does not invent a cause for the customer's predicted churn.

### Audit Trail

A compliant advisory record should contain:

* Risk probability
* Tenure
* Retrieved clause
* Top three global feature-importance signals
* Generated LLM explanation
* Validation result

This creates an auditable record of the information used to generate the recommendation.

## 🧪 Task 6 LLM Execution Status

The deterministic part of Task 6 has been completed.

For the selected test customer:

```text
Risk probability: approximately 99.22%
Tenure: 1 month
Expected clause: Clause 3
```

The actual grounded LLM call and the ungrounded comparison call have **not been fabricated**.

They remain pending until an assignment-approved generative LLM provider is available.

If an approved provider becomes available, the required workflow is:

1. Calculate the expected clause first.
2. Run the grounded call using the retrieved clause.
3. Record the exact LLM response.
4. Run the ungrounded comparison call without the playbook.
5. Record the exact response.
6. Compare the ungrounded response with the expected clause.
7. Validate the grounded response for governance compliance.

If the ungrounded call happens to identify Clause 3 correctly, it should be recorded as **correct in that run but ungrounded**, not automatically classified as hallucination.

## 📈 Monitoring Signal

After deployment, monitor the:

**Difference between predicted churn rate and actual churn rate by customer segment, monthly.**

Additional model-performance monitoring should include:

* Recall
* ROC-AUC
* F1-score
* Train/test performance gap
* Segment-level performance

A sustained deterioration in prediction quality can trigger model review or retraining.

## 💰 Cost Control

For high-volume LLM advisory generation:

* Cache the retrieved retention clauses because the same approved clause can apply to many customers.
* Batch requests where supported.
* Use an approved lower-cost model for simple, standardized advisory tasks where appropriate.
* Monitor token usage and LLM cost by segment.
* Restrict LLM calls to cases where a generated explanation provides additional business value.

## 📝 Project Files

| File                          | Purpose                                             |
| ----------------------------- | --------------------------------------------------- |
| `notebooks/01_analysis.ipynb` | Main analysis notebook                              |
| `src/data_processing.py`      | Data loading, cleaning and preprocessing            |
| `src/retention_rag.py`        | Retention playbook, retrieval and validation logic  |
| `docs/ANALYSIS_NOTES.md`      | Detailed analysis, results and governance decisions |
| `docs/MEMO.md`                | Executive one-page memo                             |
| `requirements.txt`            | Python dependencies                                 |
| `.gitignore`                  | Ignore data files and secrets                       |

## ⚠️ Important Notes

1. **Dataset:** The project uses the IBM Telco Customer Churn dataset for academic/demonstration purposes.
2. **LLM access:** No API credentials are stored in the repository.
3. **Data leakage:** Preprocessing is fitted on training data before transforming the test data.
4. **Generalization:** The Random Forest has a 14.99 percentage-point train/test accuracy gap, so post-deployment monitoring is important.
5. **Governance:** Protected demographic/family attributes are not used as causal explanations or retention reasons.
6. **LLM privacy:** The advisory layer receives only the approved allowlisted information rather than the customer's complete record.
7. **LLM execution:** Grounded and ungrounded LLM outputs are pending assignment-approved LLM access and are not fabricated in this documentation.

## 🎓 Learning Outcomes

This project demonstrates understanding of:

* End-to-end data science workflow
* Exploratory data analysis
* Data cleaning and preprocessing
* Classification modelling
* Class-imbalance considerations
* Cross-validation and model selection
* Model generalization and overfitting
* Feature-importance analysis
* Customer segmentation using KMeans
* Rule-based retrieval / RAG concepts
* Prompt governance
* Non-discrimination controls
* LLM output validation
* Model monitoring
* Cost control for high-volume AI workflows
* Executive communication of technical findings

## 📖 Documentation

For additional details, refer to:

* **`docs/ANALYSIS_NOTES.md`** — detailed analysis, modelling decisions, feature importance, segmentation, Task 6 governance, and execution status.
* **`docs/MEMO.md`** — executive one-page summary.
* **`notebooks/01_analysis.ipynb`** — analysis and modelling implementation.
* **`src/retention_rag.py`** — retention playbook and advisory logic.

## 📞 Analytical Questions

The notebook and analysis notes address questions including:

* Why is contract type correlation rather than proof of causation?
* Why can accuracy be misleading for churn prediction?
* How can train/test performance reveal overfitting?
* What does an ungrounded LLM response demonstrate?
* Why is ungrounded generation more risky in a compliance-sensitive retention workflow?
* How can demographic data leakage be prevented?
* How should churn models and segments be monitored after deployment?

---

**Last Updated:** September 6, 2026
**Status:** Analysis and modelling completed; deterministic retention retrieval completed; grounded and ungrounded GenAI execution pending assignment-approved LLM access.

