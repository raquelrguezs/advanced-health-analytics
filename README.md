# Clinical Risk Stratification for 30-Day Hospital Readmission
### Predictive Engine using Synthetic Electronic Health Records (EHR)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Executive Summary
This project demonstrates an end-to-end clinical data science pipeline for predicting 30-day hospital readmissions using a high-prevalence synthetic EHR dataset. The analysis integrates rigorous data cleansing, winsorization of clinical vitals, and comparative statistical profiling (ANOVA/Chi-Square). Optimized for clinical sensitivity, the resulting Random Forest engine achieves a **Recall of 0.98** and an **ROC-AUC of 0.8553**, prioritizing the minimization of False Negatives in a post-discharge triage scenario.

## Problem Statement
Hospital readmission is a critical healthcare quality metric and a primary driver of financial risk under the **CMS Hospital Readmissions Reduction Program (HRRP)**. Effective risk stratification at discharge enables proactive transitional care management, reducing preventable returns that strain institutional resources and impact patient morbidity.

## Objective
The primary goal is to develop a baseline risk-stratification model capable of identifying patients who require intensive post-discharge follow-up. 
- **Target**: 30-day readmission (binary).
- **Secondary Goal**: Identify statistically significant clinical drivers to inform discharge planning.

## Dataset Description
- **Source**: Synthetic Electronic Health Record (EHR) data.
- **Scope**: 12,000 records across 11 clinical and demographic variables.
- **Clinical Context**: The dataset features an elevated readmission prevalence (~90%), serving as a controlled environment to validate pipeline architecture and model sensitivity. 
- **Disclaimer**: This is a **Proof of Concept (PoC)**. In a real-world setting, readmission rates typically range between 15-25%; the current distribution is optimized for technical demonstration rather than epidemiological representation.

## Methodology
- **Data Preprocessing**: Handling of missing lab values (Hemoglobin) via median imputation and outlier management in vital signs (Systolic BP, Glucose) using winsorization to preserve clinical signals.
- **Exploratory Analysis**: Univariate and bivariate analysis focused on the correlation between Length of Stay (LoS) and readmission probability.
- **Statistical Methods**: Application of ANOVA (continuous variables) and Chi-Square tests (categorical) to validate feature relevance before modeling.
- **Modeling Approach**: Comparison between Logistic Regression (baseline for interpretability) and Random Forest Classifier (for feature interaction capture).

## Evaluation Metrics
The model is evaluated based on its utility for clinical triage, where **False Negatives** (missing an at-risk patient) are more critical than False Positives.
- **ROC-AUC**: 0.8553 (Measures discriminative power).
- **Recall (Class 1)**: 0.98 (Ensures maximum coverage of at-risk patients).
- **F1-Score (Class 1)**: 0.94 (Balance for the primary risk group).
- **Note**: Accuracy (0.90) is reported but acknowledged as secondary due to the high prevalence of readmissions in the synthetic sample.

## Key Findings
- **Statistical Significance**: Chi-Square and T-test analyses confirmed that **Diabetes** and **Stay Duration** are high-confidence indicators of readmission risk (p < 0.001).
- **Clinical Proxy**: Extended Length of Stay (LoS) acts as a reliable proxy for patient complexity and acuity in this synthetic cohort.
- **Predictive Power**: Multi-variable interactions captured by the Random Forest model outperformed the baseline Logistic Regression, particularly in handling non-linear clinical markers.

## Methodological & Clinical Limitations
- **Selection Bias**: The synthetic generator uses a simplified linear risk model, which may overstate model performance compared to real-world non-linear clinical data.
- **Lack of Longitudinality**: The model treats each admission as independent, failing to account for a patient's historical trajectory or prior readmission frequency.
- **Data Sparsity**: Real EHR data contains NLP-derived features (clinical notes) and Social Determinants of Health (SDoH), which are absent in this specific PoC.

## Project Structure
```text
├── data/               # Raw and processed synthetic clinical datasets
├── notebooks/          # Step-by-step EDA and Statistical Profiling
├── src/                # Modular Python scripts for data processing and modeling
├── reports/            # Technical and Executive analysis
├── tests/              # Basic unit tests for the scoring functions
└── requirements.txt    # Environment dependencies
```

## Reproducibility / How to Run
- **Environment**: Python 3.10+
- **Installation**: `pip install -r requirements.txt`
- **Execution Order**:
  1. Generate data: `python src/generate_clinical_data.py`
  2. Run Analysis: Execute Jupyter Notebooks in `notebooks/` sequentially (01 to 04).
- **Expected Output**: A cleaned CSV in `data/processed/` and a visual assessment of model performance (ROC and Confusion Matrix) in notebook 04.

## Future Improvements
- Implement **SMOTE or Class Weighting** to handle realistic (lower) readmission prevalence.
- Incorporate **Temporal Cross-Validation** to simulate prospective deployment.
- Feature engineering of "Time-since-last-discharge" to capture longitudinal risk.

---
**Raquel Rodriguez** – Clinical Data Analyst & DS Portfolio
[LinkedIn](https://www.linkedin.com/in/raquel-rodriguez) | [Professional Portfolio](https://github.com/raquelrodriguez)
