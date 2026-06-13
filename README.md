# Health Insurance Claim Prediction & Interactive Analytics Dashboard
### Advanced ML Stacking Ensemble for Risk Assessment


[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Performance](https://img.shields.io/badge/Gini-0.2860-success?style=flat-square&logo=chart-line)](https://github.com/)

**Team Zebra:**  
Om Chauhan & Lakshit Vedant  

**Competition:**  
Zerve AI Datathon | Techfest IIT Bombay | December 2025  

**Final Score:** 0.2860 Normalized Gini

*Engineering a high-performance predictive engine for quantifying policyholder risk, now supercharged with a full-stack, enterprise-grade inference dashboard.*

---

## 🌟 Advanced Architecture & Dashboard Features

We completely overhauled the project to transition from a static machine learning model into a **full-stack, production-grade intelligence application**.

* **Live What-If Scenario Builder**: Replaced static form inputs with interactive, real-time sliders. Adjusting patient age, BMI, or claim history instantly triggers a live inference call to the FastAPI backend, recalculating risk in milliseconds.
* **Explainable AI (XAI) Clinical PDF Reports**: The system acts as an automated underwriter. Clicking "Export PDF" instantly generates a perfectly formatted, 1-page clinical text document using `jsPDF`. The system translates complex SHAP values into plain English sentences to justify the AI's decision to medical staff.
* **Live Inference Database Logging**: Implemented a real-time `SQLite` database on the backend (`predictions_history` table). Every time the model makes a prediction, a unique `Patient ID` is generated and logged, allowing for live tracking of underwriting activity.
* **Premium 5-Column Dashboard Architecture**: Redesigned the analytics layout into a tight, highly optimized grid. 
  * Features a brand new **Population Risk Distribution** analytics module, showing the exact percentage breakdown of Low, Medium, and High-risk patients dynamically evaluated by the system.
  * A live **Recent Patient Evaluations Table** streaming directly from the SQLite database.
* **Gemini-Powered Chat Assistant**: Integrated an interactive floating chat panel connected to a Gemini AI endpoint, allowing users to "chat with the dashboard" and ask questions about the underlying ML model or underwriting procedures.
* **Refined Hero Layout**: A seamless, wide 3-column top section ensuring zero wasted screen space and an incredibly premium aesthetic.

---

## Table of Contents

- [Overview](#overview)
- [Interactive Web Dashboard](#interactive-web-dashboard)
- [The 4-Pillar Dashboard Architecture](#the-4-pillar-dashboard-architecture)
- [Technical Stack](#technical-stack)
- [Key ML Features](#key-ml-features)
- [Performance & Optimization Journey](#performance--optimization-journey)
- [Installation & Quick Start](#installation--quick-start)
- [Pipeline Architecture Deep Dive](#pipeline-architecture-deep-dive)
- [Feature Intelligence Insights](#feature-intelligence-insights)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Metrics & Evaluation](#metrics--evaluation)

---

## Overview

This repository contains an end-to-end machine learning system for predicting health insurance claims, complete with a **fully interactive, production-ready web dashboard**. Built with production-grade code quality and rigorous validation strategies, it combines state-of-the-art gradient boosting algorithms with advanced ensemble techniques, all wrapped in a premium UI designed for stakeholder presentations and technical interviews.

### Problem Statement

Predict the true probability of a customer filing a health insurance claim within the next fiscal year based on 50 anonymized features, ranging from biometric data to historical policy interactions.

### Business Value

| Pillar | Outcome |
| :--- | :--- |
| **Optimized Pricing** | Better risk stratification allowing for hyper-personalized premium pricing. |
| **Fraud Detection** | Early identification of statistically anomalous claim patterns. |
| **Resource Allocation** | Efficient operations by predicting peak claim volumes and allocating adjusters. |
| **Proactive Care**| Flagging high-risk patients for targeted wellness and preventative health programs before expensive claims occur. |

---

## Interactive Web Dashboard

To present our model to stakeholders, judges, and technical interviewers, we engineered a fully interactive, production-ready web application. This dashboard serves as both a live prediction engine and a comprehensive technical walkthrough of our entire machine learning pipeline. 

We avoided standard, boring Jupyter Notebook presentations in favor of a customized, high-performance web app that demonstrates immediate real-world value.

### The 4-Pillar Dashboard Architecture

#### 1. Home: Live Prediction Engine & Database
- **Interactive "What-If" Sliders**: A sleek, user-friendly interface to manipulate patient data (Age, BMI, Smoking status, Prior Claims, etc.) on the fly.
- **Real-Time API Inference**: Connects to the FastAPI backend to run the input through the live Stacking Ensemble pipeline in milliseconds.
- **Explainable AI (SHAP) PDF Generator**: Automatically translates the model's complex SHAP value outputs into human-readable clinical justifications, generating a professional, downloadable PDF Underwriting Report on demand.
- **Live SQLite Feed**: The dashboard connects to a live backend database, streaming the 5 most recent underwriting predictions directly onto the screen.

#### 2. Model Development: Architecture Roadmap
- **Interactive Pipeline Visualization**: A fully responsive, glowing "roadmap" alternating flowchart that visually breaks down the entire pipeline from raw data to isotonic calibration.
- **Glassmorphic UI**: Premium, translucent glass-like cards that seamlessly adapt to both Light and Dark mode user preferences.
- **Educational Sidebars**: Contextual explanations diving deep into the "Why" behind the architecture (e.g., explaining why SMOTE balancing prevents bias, and how the Meta-Learner learns which base algorithm to trust).

#### 3. Analytics & Results: The Justification
- **Evaluation Matrix**: Color-coded, premium data tables breaking down Out-Of-Fold (OOF) Gini and AUC scores across LightGBM, XGBoost, and CatBoost.
- **Performance Visualizations**:
  - **Journey Area Chart**: Tracks the Gini progression incrementally from the baseline score to the final podium-level 0.2860 score.
  - **5-Fold Stability Line Chart**: Proves robustness and a complete lack of data leakage across all 5 cross-validation folds.
  - **Multi-Metric Radar**: Highlights production readiness across evaluation criteria (Gini, AUC, Brier Score).

#### 4. Feature Intelligence: Exploratory Data Analysis
- **Nightingale Rose Chart**: Stunning radial visualization of the extreme 85:15 class imbalance, directly justifying our SMOTE implementation.
- **KDE Overlap Plots**: Interactive area charts showing the distribution overlap (e.g., BMI) between Claim and No-Claim classes, mathematically proving the necessity of non-linear gradient boosted trees over simple logistic regression.
- **Interactive Correlation Matrix**: A massive, cool-blue heatmap detailing collinearity between all 50 features, which drove our feature selection and interaction engineering strategy.

---

## Technical Stack

### Frontend Architecture
- **React.js 18**: Component-driven UI framework utilized for rapid, stateful UI development.
- **Tailwind CSS 4**: Utility-first styling with advanced custom gradients, complex grid layouts, and seamless dark/light mode integration.
- **html-to-image & jsPDF**: Used together to parse DOM nodes and natively generate highly structured, customized clinical PDF reports.
- **ECharts (Apache)**: High-performance, interactive data visualizations (`echarts-for-react`) powering the analytics and Feature Intelligence tabs.
- **Lucide React**: Premium, lightweight SVG iconography suite.
- **Vite**: Ultra-fast frontend build tooling and Hot Module Replacement (HMR).

### Backend Architecture
- **FastAPI**: Asynchronous Python web framework serving the ML model via REST endpoints with sub-10ms latency.
- **SQLite**: Lightweight, ultra-fast relational database tracking live historical predictions, patient IDs, and risk scores.
- **Uvicorn**: Lightning-fast ASGI web server implementation.
- **Joblib**: Efficient serialization and deserialization of the trained LightGBM meta-learner, base models, and Isotonic scalers.
- **Pandas / NumPy**: Real-time data manipulation and on-the-fly feature engineering for inference requests.
- **CORS Middleware**: Securely linking the separate React frontend port (5173) to the FastAPI backend port (8000).

---

## Key ML Features

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
- Modular REST API
- React Web Interface & PDF Gen
- Live SQLite DB Logging
- Visualization suite

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
| Baseline Gini | 0.2599 | - |
| **Improvement** | **+10.04%** | 🚀 |

### Optimization Journey

```python
# Performance progression
stages = {
    'Raw Baseline':               0.2599,
    '+ Feature Engineering':      0.2749,  # +0.0121
    '+ Optuna Tuning':            0.2832,  # +0.0083
    '+ Feature Selection':        0.2834,  # +0.0002
    '+ Stacking Meta-Learner':    0.2848,  # +0.0014
    '+ Expanded GroupBy Stats':   0.2860,  # +0.0012
}
```

### The Ablation Study

We conducted a rigorous ablation study to evaluate the impact of Advanced Feature Engineering vs Mathematical Ensembling:

| Strategy | Score | Impact vs Previous | Conclusion |
| :--- | :--- | :--- | :--- |
| **Raw Baseline (No Feature Eng)** | 0.2599 | - | Weak starting point |
| **Intermediate (Top 65% Features)** | 0.2834 | +0.0235 | Strong Base Models |
| **Test 1: GroupBy Features** | 0.2850 | +0.0016 | Highly Predictive |
| **Test 2: Optuna Meta-Tuning** | 0.2829 | -0.0005 | Overfitting |
| **Test 3: Rank Blending** | 0.2820 | -0.0014 | Destructive to signal |
| **SLSQP Weight Optimization** | 0.2816 | -0.0018 | Linear blending failed |
| **FINAL RUN** | **0.2860** | **+0.0026** | **Perfect Synergy** |

**Final Architecture Decision:** The mathematical linear blending (SLSQP) failed because the base models were highly correlated. The original LightGBM Meta-Learner with a shallow tree (`max_depth=3`) was able to capture the non-linear synergy between the base models. By combining this Meta-Learner with expanded GroupBy statistical features (`min`, `max`, `mean`, `std`), we successfully breached the 0.2860 threshold.

---

## Installation & Quick Start

### Prerequisites

```bash
Node.js 18.x+
Python 3.9+
pip 21.0+
```

### Clone Repository

```bash
git clone https://github.com/OmChauhan2023/Health-Insurance-Claim-Prediction-Model.git
cd Health-Insurance-Claim-Prediction-Model
```

### 1. Start the FastAPI Backend

Open a terminal and set up the Python environment:

```bash
cd backend
python -m venv venv

# Activate Virtual Environment
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows

# Install Requirements
pip install -r requirements.txt

# Run the API Server
python -m uvicorn main:app --port 8000 --reload
```
The backend API is now running on `http://localhost:8000`.

### 2. Start the React Frontend Dashboard

Open a *new* second terminal:

```bash
cd frontend

# Install Node dependencies
npm install

# Run the Vite Dev Server
npm run dev
```
The interactive UI is now running on `http://localhost:5173`. Open this URL in your browser to explore the full dashboard!

---

## Pipeline Architecture Deep Dive

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

### 1. Missing Value Imputation
Medical data is notoriously messy. Our pipeline utilizes an intelligent grouped-median imputation strategy for numerical values (e.g., imputing a missing BMI based on the median BMI for that specific age and gender group, rather than a global mean) and a separate distinct 'Unknown' category encoding for missing categorical strings to allow tree-based algorithms to map missingness as a valid predictive branch.

### 2. Synthetic Minority Over-sampling Technique (SMOTE)
To combat the severe 85:15 target imbalance, we utilized a custom SMOTE pipeline. Rather than over-sampling to a 50:50 ratio (which creates synthetic noise and destroys probability calibration), we implemented a conservative 0.05 SMOTE ratio paired with a 0.3 random under-sampling of the majority class. This provided enough signal for the trees to build deep leaves predicting 'Claim' without overwhelming the dataset with synthetic artifacts.

---

## Feature Intelligence Insights

Extensive Exploratory Data Analysis (EDA) drove our engineering decisions. (These insights are dynamically visualized in the **Feature Intelligence** tab of the dashboard).

- **Multi-Collinearity Discovery**: We observed an extreme Pearson correlation (`0.82`) between the `Premium_Cost` and `Prior_Claims`. This multicollinearity confuses traditional linear models and can lead to feature importance distortion in XGBoost. To resolve this, we engineered an interaction term `Premium_Per_Claim` and utilized strict tree L2 regularization (`reg_lambda`).
- **Distribution Overlap**: KDE plotting of the `BMI` feature against the target variable revealed near-perfect overlap between Claimants and Non-Claimants. This mathematical overlap proved that simple linear boundaries (e.g., Logistic Regression) would categorically fail, necessitating the use of non-linear gradient-boosted spatial splits.

---

## Model Details

Our final ensemble utilizes three gradient boosting frameworks optimized for their unique architectural strengths:

### Base Level 1
1. **LightGBM**: Configured for leaf-wise growth, enabling highly granular splits on continuous variables. Due to its histogram-based binning, it is the fastest of the three base models.
2. **XGBoost**: Configured for depth-wise growth with strict `max_depth` constraints, acting as the stabilizing anchor in the ensemble, providing incredibly robust and generalized predictions resistant to outliers.
3. **CatBoost**: Configured for symmetric tree generation and ordered boosting, excelling at handling the remaining categorical feature interactions without requiring extensive One-Hot Encoding overhead.

### Meta Level 2
- **LightGBM Meta-Learner**: We abandoned mathematical linear blending (like SLSQP) because the base models were highly correlated. Instead, we used a shallow LightGBM model (`max_depth=3`, `num_leaves=7`) trained purely on the Out-Of-Fold (OOF) prediction probabilities of the three base models. This architecture successfully captures the non-linear synergies between the base models without succumbing to the severe overfitting risks identified during our ablation study.

---

## Project Structure

```text
Health-Insurance-Claim-Prediction-Model/
│
├── backend/
│   ├── api/
│   │   └── routes.py                  # FastAPI REST endpoints + SQLite
│   ├── main.py                        # Uvicorn server entry point
│   ├── predictions.db                 # Live SQL Database for History
│   ├── requirements.txt               # Backend Python dependencies
│   └── models/                        # Saved Joblib ensemble weights
│
├── frontend/
│   ├── src/
│   │   ├── components/                # React UI Components
│   │   │   ├── Dashboard.jsx          # Live Prediction + DB History UI
│   │   │   ├── PredictionForm.jsx     # What-If Sliders + PDF Export Engine
│   │   │   ├── ChatPanel.jsx          # Gemini LLM Integration
│   │   │   ├── ModelDev.jsx           # Architecture Roadmap 
│   │   │   ├── Analytics.jsx          # Results & Metrics Grid
│   │   │   └── PlotsGallery.jsx       # Interactive Feature EDA
│   │   ├── App.jsx                    # Main Routing Component
│   │   └── index.css                  # Tailwind Entry & Custom Utilities
│   ├── package.json                   # Node.js dependencies
│   └── vite.config.js                 # Vite bundler config
│
├── ml_pipeline/
│   ├── src/
│   │   ├── feature_engineering.py     # GroupBy and Poly features
│   │   ├── preprocessing.py           # Data cleaning & SMOTE
│   │   └── models.py                  # XGBoost/LGBM/CatBoost classes
│   └── scripts/
│       └── train_kfold.py             # Offline training execution script
│
└── README.md                          # Comprehensive documentation
```

---

## Metrics & Evaluation

### Normalized Gini Coefficient

The Gini coefficient is the industry standard for credit risk and insurance prediction because it evaluates the model's ability to perfectly rank-order the population by risk, rather than simply measuring absolute accuracy.

```python
def normalized_gini(y_true, y_pred):
    """
    Primary metric for insurance risk ranking.
    
    Range: [0, 1]
    - 1.0: Perfect ranking
    - 0.5: Random chance
    - 0.0: Worst possible ranking
    
    Relation to AUC: Gini = 2 × AUC - 1
    """
    gini_val = gini(y_true, y_pred)
    gini_max = gini(y_true, y_true)
    return gini_val / gini_max
```

### Isotonic Calibration

A model with a high Gini score can perfectly sort customers from highest to lowest risk, but its absolute output probabilities (e.g., `0.99` vs `0.01`) might be wildly inaccurate. To make the model usable in a production business environment (where actual financial premiums are calculated based on raw probability), we passed the Meta-Learner output through an `IsotonicRegression` calibrator. This ensures that when the model outputs a 15% probability of a claim, mathematically, exactly 15% of that cohort will historically file a claim.

---

## References

1. **SMOTE**: Chawla, N. V., et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique"
2. **XGBoost**: Chen, T., & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System"
3. **LightGBM**: Ke, G., et al. (2017). "LightGBM: A Highly Efficient Gradient Boosting Decision Tree"
4. **CatBoost**: Prokhorenkova, L., et al. (2018). "CatBoost: unbiased boosting with categorical features"
5. **Calibration**: Niculescu-Mizil, A., & Caruana, R. (2005). "Predicting good probabilities with supervised learning"
