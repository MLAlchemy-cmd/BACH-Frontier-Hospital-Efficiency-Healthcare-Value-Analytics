# BACH Frontier — Hospital Efficiency & Healthcare Value Analytics

**Healthcare Analytics | Machine Learning | Data Envelopment Analysis | Predictive Modeling | Optimization**

*University of Minnesota — Carlson Interdisciplinary Healthcare Analytics Competition 2026*

## Project Overview

BACH Frontier is an end-to-end healthcare analytics project designed to evaluate hospital operational efficiency, identify factors associated with high-performing hospitals, and explore opportunities for improving healthcare quality and financial sustainability.

Using publicly available hospital financial and clinical quality data, the project combines **Data Envelopment Analysis (DEA), statistical regression, gradient-boosting models, and scenario-based optimization** to investigate the relationship between hospital costs, quality outcomes, and operational performance.

The analysis considers both safety-net and non-safety-net hospitals, with particular attention to healthcare accessibility, financial resilience, and resource utilization.

## Analytical Framework

<img width="848" height="492" alt="image" src="https://github.com/user-attachments/assets/007ec03a-8ac7-4092-8667-80dd39a6ae33" />


The project follows four analytical phases:

1. **Data Acquisition and Preparation:** Integrating hospital financial records, quality indicators, and operational variables.
2. **Hospital Classification:** Identifying safety-net hospitals and categorizing hospitals by efficiency performance.
3. **Multi-Method Analysis:** Applying DEA, multivariable regression, and machine learning.
4. **Impact and Scenario Analysis:** Evaluating potential operational improvements and Medicaid funding-shock scenarios.

## Dataset and Data Engineering

**Data sources**
- CMS Healthcare Cost Report Information System (HCRIS)
- CMS hospital quality and outcomes data
- Hospital financial and operational indicators

**Dataset characteristics**
- 158,688 HCRIS hospital-year records
- 621 source variables
- 42,625 records retained for the 2015–2021 analysis in the primary notebook
- Clinical quality indicators covering six conditions: AMI, heart failure, pneumonia, COPD, stroke, and CABG

**Data processing**
- Missing-value handling and outlier screening
- Data consistency checks
- Financial and operational feature engineering
- Medicaid discharge-share calculations
- Hospital efficiency and quality-score integration
- Safety-net and non-safety-net subgroup analysis

The competition presentation additionally describes a separate non-safety-net analysis. Its combined dataset totals should be interpreted separately from the primary notebook's filtered analytical sample.

## Methodology

### 1. Data Envelopment Analysis (DEA)

DEA was used to benchmark relative hospital efficiency by comparing resource utilization and healthcare performance.

The analysis investigates how hospitals convert financial and operational resources into healthcare services and quality outcomes.

### 2. Hospital Efficiency Distribution

<img width="642" height="517" alt="image" src="https://github.com/user-attachments/assets/05d250e5-3dfd-4088-99c8-6a6fa5c8de75" />


This visualization compares the distribution of DEA efficiency scores between safety-net and non-safety-net hospitals.

It highlights variation in relative efficiency and supports further investigation of differences in hospital operating characteristics.

### 3. Regression and Statistical Analysis

Multivariable regression was used to investigate associations between hospital characteristics and efficiency.

Variables examined include hospital size, occupancy, financial performance, and operational characteristics.

The primary regression analysis reported an **R² of approximately 0.49**, indicating that the model explained about 49% of the variation in the modeled efficiency outcome.

These relationships are observational associations and should not be interpreted as causal effects.

### 4. Predictive Machine Learning

A gradient-boosting classification model was developed to distinguish high- and low-efficiency hospital groups using structural and financial features.

**Reported evaluation results**

| Metric | Result |
|---|---|
| Accuracy | 93% |
| ROC-AUC | 0.983 |
| Test set | 594 records |
| Evaluation | Balanced hold-out classification |

The evaluation used a stratified random split. These metrics describe classification performance within the analyzed dataset, not independently validated performance on future years or previously unseen hospitals.

### 5. Cost–Quality Efficiency Frontier

<img width="983" height="705" alt="image" src="https://github.com/user-attachments/assets/c30bf847-9478-43ce-afbe-85c6252bf6a8" />


The cost–quality visualization explores the relationship between hospital quality scores and cost per case.

It highlights selected frontier hospitals and uses Medicaid patient share to illustrate variation in hospital characteristics.

The displayed example focuses on acute myocardial infarction (AMI) in 2017.

### 6. Medicaid Funding-Shock Scenario Analysis

A financial scenario analysis was conducted to explore how hospital revenue reductions could affect financial sustainability and whether modeled operational improvements might offset part of the losses.

<img width="1212" height="715" alt="image" src="https://github.com/user-attachments/assets/5c78a707-ffe2-4007-8940-bc9224d928ea" />


The illustrated example considers:
- Baseline hospital income
- Modeled revenue reduction
- Potential optimization savings
- Post-optimization income

The scenario illustrates financial sensitivity under assumed conditions. It is not evidence of actual realized savings.

## Key Findings

The project demonstrates how combining efficiency analysis, predictive modeling, and financial scenarios can support hospital performance assessment.

Key analytical observations include:

- Hospital efficiency varies substantially across institutions.
- Structural and operational characteristics are associated with differences in efficiency.
- Gradient boosting can distinguish efficiency-defined hospital groups within the evaluated sample.
- Financial scenario analysis can illustrate potential hospital vulnerability to funding reductions.
- Cost, quality, and access considerations should be examined together when assessing healthcare value.

The competition presentation also explored broader projected financial and clinical impacts. Those estimates represent modeled scenarios rather than observed real-world outcomes.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Gradient Boosting |
| Statistical Analysis | Regression, DEA |
| Visualization | Matplotlib, Seaborn |
| Development | Jupyter Notebook, Databricks |
| Data Sources | CMS HCRIS, CMS Quality Data |


The repository structure reflects the intended organization of the project. Some analytical inputs, including previously computed DEA efficiency scores, may need to be obtained or regenerated separately to reproduce the complete analysis.

## Limitations

- DEA efficiency measures are relative to the chosen comparison group, inputs, and outputs.
- The classification evaluation uses a random stratified hold-out rather than an independent future-year or hospital-level validation.
- The predictive target is derived from efficiency analysis; potential overlap between target construction and model features should be assessed.
- Financial and clinical impact projections depend on scenario assumptions and should not be treated as realized outcomes.
- Results from different hospital subgroups and analytical samples are not directly interchangeable.

## Project Context

Developed for the **University of Minnesota Carlson Interdisciplinary Healthcare Analytics Competition 2026**.

The project combines healthcare data engineering, statistical analysis, operations research, machine learning, and decision-support visualization to explore hospital efficiency and healthcare value.

 
M.S. Data Science — University of Minnesota, Twin Cities

**Focus Areas:** Healthcare AI, Applied Machine Learning, Statistical Modeling, and Data Analytics.
