# Hospital Readmission Risk Engine (HRRE)
### Clinical Risk Stratification using Electronic Health Records (EHR)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🩺 Executive Summary
Predicting 30-day hospital readmission is a cornerstone of healthcare quality management. This project implements a full clinical data science pipeline that processes synthetic Electronic Health Records (EHR) to identify patients at high risk of returning to the hospital. 

Unlike generic predictive models, this engine handles **biased clinical prevalence** (~90% readmission rate in synthetic data) by focusing on **ROC-AUC** and **F1-Score**, providing hospitals with a reliable risk-stratification tool to prioritize post-discharge interventions.

## 📊 The Clinical & Business Problem
Under the **CMS Hospital Readmissions Reduction Program (HRRP)**, hospitals face significant financial penalties for high readmission rates. Identifying at-risk patients *at discharge* allows for:
- Targeted home-care nursing.
- Proactive medication management.
- Reduction of Bed-Blocking and emergency department strain.

## 🧪 Methodology & Tech Stack
- **Data Engineering**: Outlier detection in vital signs (Systolic BP, Glucose) and imputation of missing lab markers (Hemoglobin).
- **Statistical Profiling**: ANOVA and Chi-Square analysis to identify statistically significant clinical drivers.
- **Predictive Modeling**: Comparison between Logistic Regression (interpretability) and Random Forest (performance).
- **Interpretability**: Feature importance analysis focused on Length of Stay (LoS) and Diabetes comorbidities.

## 📈 Model Performance & Clinical Validation
Evaluation was performed using a hold-out test set (20%). The model prioritizes **Recall for high-risk patients** to ensure actionable intervention coverage.

| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Stable (Low Risk)** | 0.35 | 0.12 | 0.18 | 223 |
| **Readmitted (High Risk)** | 0.91 | 0.98 | 0.94 | 2153 |
| **Metric Overview** | **ROC-AUC: 0.855** | **Accuracy: 0.90** | | |

> **Analyst Note on Sensitivity**: In a clinical context, a False Positive (treating a low-risk patient as high-risk) is often less costly than a False Negative (missing a patient who will deteriorate). The model is tuned for high sensitivity.

## 📂 Project Structure
```text
├── data/               # Raw and processed CSVs
├── notebooks/          # Exploratory and statistical clinical analysis
├── src/                # Modular logic (Data cleansing & Scorer)
├── reports/            # Executive summaries for stakeholders
├── tests/              # Unit testing for risk-scoring functions
└── requirements.txt    # Dev environment dependencies
```

## 🚀 Reproduction & Quickstart
1. **Setup Env**: `pip install -r requirements.txt`
2. **Data Generation**: `python src/generate_clinical_data.py`
3. **Exploration**: Review `notebooks/01_clinical_data_cleansing.ipynb`
4. **Scoring**: Use the `predict_readmission_risk` function in `src/model_utils.py` (simulated).

---
**Raquel Rodríguez** – Clinical Data Analyst & DS Portfolio
[LinkedIn](https://www.linkedin.com/in/raquel-rodriguez) | [Professional Portfolio](https://github.com/raquelrodriguez)
