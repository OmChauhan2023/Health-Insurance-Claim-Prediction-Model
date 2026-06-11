<div align="center">

# Health Insurance Claim Prediction
### Advanced ML Stacking Ensemble for Risk Assessment

[![Model Version](https://img.shields.io/badge/Version-1.2.0-blueviolet?style=flat-square)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Performance](https://img.shields.io/badge/Gini-0.2860-success?style=flat-square&logo=chart-line)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

**Developed by Team Zebra: Om Chauhan & Lakshit Vedant**
**Zerve AI Datathon | Techfest IIT Bombay (December 2025)**

Engineering a high-performance predictive engine for quantifying policyholder risk and claim probability.

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Performance & Optimization Journey](#performance--optimization-journey)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Pipeline Architecture](#pipeline-architecture)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Metrics & Evaluation](#metrics--evaluation)
- [References](#references)

---

## Overview

This repository contains an end-to-end machine learning system for predicting health insurance claims. Built with production-grade code quality and rigorous validation strategies, it combines state-of-the-art gradient boosting algorithms with advanced ensemble techniques.

### Problem Statement

Predict the probability of a customer filing a health insurance claim based on 50 anonymized features. 

### Business Value

| Pillar | Outcome |
| :--- | :--- |
| **Optimized Pricing** | Better risk stratification |
| **Fraud Detection** | Early identification |
| **Resource Allocation** | Efficient operations |
| **Customer Segmentation**| Personalized products |

---

## Key Features

<table>
<tr>
<td>

### Engineering
- 117 engineered features
- Advanced GroupBy Statistical features (`mean`, `std`, `min`, `max`)
- Target encoding (smoothing=10)
- SMOTE + under-sampling
- Top 65% feature selection
- Isotonic calibration

</td>
<td>

### Models
- LightGBM (leaf-wise)
- XGBoost (depth-wise)
- CatBoost (ordered boosting)
- LightGBM Meta-Learner (Stacking)
- Deep Learning (Ablated)

</td>
</tr>
<tr>
<td>

### Validation
- Stratified 5-Fold Cross Validation
- Out-of-Fold (OOF) Ensembling
- No data leakage
- Gini coefficient metric
- Calibrated probabilities

</td>
<td>

### Production
- Reproducible (seed=42)
- Modular architecture
- Comprehensive logging
- Visualization suite
- Easy deployment

</td>
</tr>
</table>

---

## Performance & Optimization Journey

Our optimization journey involved a strict ablation study to isolate the impact of different modeling techniques and feature engineering strategies. By stripping away underperforming components and maximizing winning strategies, we successfully hit our exact target Gini score.

### Leaderboard

| Metric | Score | Rank |
|--------|-------|------|
| **Final OOF Gini** | **0.2860** | 🥇 |
| Baseline Gini | 0.2628 | - |

### The Ablation Study

We conducted a rigorous ablation study to evaluate the impact of Advanced Feature Engineering vs Mathematical Ensembling:

| Strategy | Score | Impact vs Baseline | Conclusion |
| :--- | :--- | :--- | :--- |
| **Baseline (Top 65% Features)** | 0.2834 | - | Strong Base Models |
| **Test 1: GroupBy Features** | 0.2850 | +0.0016 | Highly Predictive |
| **Test 2: Optuna Meta-Tuning** | 0.2829 | -0.0005 | Overfitting |
| **Test 3: Rank Blending** | 0.2820 | -0.0014 | Destructive to signal |
| **SLSQP Weight Optimization** | 0.2816 | -0.0018 | Linear blending failed |
| **FINAL RUN** | **0.2860** | **+0.0026** | **Perfect Synergy** |

**Final Architecture Decision:** The mathematical linear blending (SLSQP) failed because the base models were highly correlated. The original LightGBM Meta-Learner with a shallow tree (`max_depth=3`) was able to capture the non-linear synergy between the base models. By combining this Meta-Learner with expanded GroupBy statistical features (`min`, `max`, `mean`, `std`), we successfully breached the 0.2860 threshold.

---

## Installation

### Prerequisites

```bash
Python 3.8+
pip 21.0+
```

### Clone Repository

```bash
git clone https://github.com/OmChauhan2023/Health-Insurance-Claim-Prediction-Model.git
cd Health-Insurance-Claim-Prediction-Model
```

### Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

---

## Quick Start

### 1. Prepare Data

```bash
# Place your data files in data/ directory
data/
├── training_data.csv
└── test_data.csv
```

### 2. Run Complete Pipeline

```python
python scripts/train_kfold.py
```

### 3. Output

```bash
outputs/
├── submission_true_final.csv      # Predictions
├── meta_model.joblib              # Stacking Learner
├── calibrator.joblib              # Isotonic Calibrator
```

---

## Pipeline Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                           RAW DATA                            │
│                    (476,169 × 50 features)                    │
└──────────────────────────────┬────────────────────────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │    5-FOLD STRATIFIED      │
                 │     CROSS-VALIDATION      │
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │    FEATURE ENGINEERING    │
                 │(GroupBy Stats, Polynomial)│
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │        RESAMPLING         │
                 │ SMOTE (0.05) + Under (0.3)│
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │     FEATURE SELECTION     │
                 │       (Top 65%)           │
                 └─────────────┬─────────────┘
                               ↓
        ┌──────────────────────┼──────────────────────┐
        ↓                      ↓                      ↓
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   LightGBM    │      │    XGBoost    │      │   CatBoost    │
└───────────────┘      └───────────────┘      └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │  STACKING META-LEARNER    │
                 │  (LightGBM max_depth=3)   │
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │   ISOTONIC CALIBRATION    │
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │     FINAL PREDICTIONS     │
                 │      OOF Gini: 0.2860     │
                 └───────────────────────────┘
```

---

## Model Details

Our final ensemble utilizes three gradient boosting frameworks optimized for their unique architectural strengths:

### Base Level 1
1. **LightGBM**: Configured for leaf-wise growth, enabling highly granular splits on continuous variables. 
2. **XGBoost**: Configured for depth-wise growth with histogram binning for stable, robust predictions.
3. **CatBoost**: Configured for symmetric tree generation and ordered boosting, excelling at categorical feature interactions.

### Meta Level 2
- **LightGBM Meta-Learner**: A shallow LightGBM model (`max_depth=3`, `num_leaves=7`) trained purely on the Out-Of-Fold (OOF) predictions of the three base models. This captures the non-linear synergies between the models without succumbing to the severe overfitting risks identified during our ablation study.

---

## Project Structure

```text
zebra/
│
├── data/
│   ├── training_data.csv              # Training dataset
│   └── test_data.csv                  # Test dataset
│
├── logs/
│   └── *.log                          # Ablation and testing logs
│
├── src/
│   ├── feature_engineering.py         # GroupBy and Poly features
│   ├── preprocessing.py               # Data cleaning
│   └── models.py                      # Model definitions
│
├── scripts/
│   └── train_kfold.py                 # Main execution pipeline
│
├── outputs/
│   └── submission_true_final.csv      # Final predictions
│
├── requirements.txt                   # Dependencies
└── README.md                          # This file
```

---

## Metrics & Evaluation

### Normalized Gini Coefficient

```python
def normalized_gini(y_true, y_pred):
    """
    Primary metric for insurance risk ranking.
    
    Range: [0, 1]
    - 1.0: Perfect ranking
    - 0.5: Random
    - 0.0: Worst possible
    
    Relation to AUC: Gini = 2 × AUC - 1
    """
    gini_val = gini(y_true, y_pred)
    gini_max = gini(y_true, y_true)
    return gini_val / gini_max
```

---

## References

1. **SMOTE**: Chawla, N. V., et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique"
2. **XGBoost**: Chen, T., & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System"
3. **LightGBM**: Ke, G., et al. (2017). "LightGBM: A Highly Efficient Gradient Boosting Decision Tree"
4. **CatBoost**: Prokhorenkova, L., et al. (2018). "CatBoost: unbiased boosting with categorical features"
5. **Calibration**: Niculescu-Mizil, A., & Caruana, R. (2005). "Predicting good probabilities with supervised learning"
