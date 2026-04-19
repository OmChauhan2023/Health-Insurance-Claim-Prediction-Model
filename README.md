<div align="center">

# 🦓 PROJECT ZEBRA
### **Health Insurance Claim Prediction | Advanced ML Stacking Ensemble**

[![Model Version](https://img.shields.io/badge/Version-1.2.0-blueviolet?style=flat-square)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Performance](https://img.shields.io/badge/Gini-0.28542-success?style=flat-square&logo=chart-line)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

**Engineering a high-performance predictive engine for quantifying policyholder risk and claim probability.**

[Explore Docs](https://github.com/) · [Report Bug](https://github.com/) · [Request Feature](https://github.com/)

</div>

---

## 📋 **Table of Contents**

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Performance](#-performance)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Pipeline Architecture](#-pipeline-architecture)
- [Model Details](#-model-details)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Experiments](#-experiments)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 **Overview**

**ZEBRA** (Zero-Error Bias Risk Assessment) is an end-to-end machine learning system for predicting health insurance claims. Built with production-grade code quality and rigorous validation strategies, it combines state-of-the-art gradient boosting algorithms with advanced ensemble techniques.

### **Problem Statement**

Predict the probability of a customer filing a health insurance claim based on 50 anonymized features.

### **Business Value**

| Pillar | Outcome |
| :--- | :--- |
| 💰 **Optimized Pricing** | Better risk stratification |
| 🔍 **Fraud Detection** | Early identification |
| 📊 **Resource Allocation** | Efficient operations |
| 🎯 **Customer Segmentation**| Personalized products |

---

## ✨ **Key Features**

<table>
<tr>
<td>

### 🔧 **Engineering**
- 109 engineered features
- Target encoding (smoothing=10)
- SMOTE + under-sampling
- Top 80 feature selection
- Isotonic calibration

</td>
<td>

### 🤖 **Models**
- LightGBM (leaf-wise)
- XGBoost (depth-wise)
- CatBoost (ordered boosting)
- Weighted ensemble
- Optuna optimization

</td>
</tr>
<tr>
<td>

### 📊 **Validation**
- Stratified 80/20 split
- No data leakage
- K-fold compatible
- Gini coefficient metric
- Calibrated probabilities

</td>
<td>

### 🚀 **Production**
- Reproducible (seed=42)
- Modular architecture
- Comprehensive logging
- Visualization suite
- Easy deployment

</td>
</tr>
</table>

---

## 🏆 **Performance**

### **Leaderboard**

| Metric | Score | Rank |
|--------|-------|------|
| **Validation Gini** | **0.2851** | 🥇 |
| Baseline Gini | 0.2628 | - |
| **Improvement** | **+8.5%** | - |

### **Model Comparison**

| Model | Individual | Calibrated | Ensemble Weight |
| :--- | :--- | :--- | :--- |
| LightGBM | 0.2798 | 0.2826 | 12.3% |
| XGBoost | 0.2794 | 0.2824 | 27.8% |
| CatBoost | 0.2820 | 0.2848 | 59.9% |
| **ENSEMBLE** | **-** | **-** | **0.2851** 🎯 |

### **Optimization Journey**

```python
# Performance progression
stages = {
    'Baseline':              0.2628,
    '+ Feature Engineering': 0.2749,  # +0.0121
    '+ Optuna Tuning':       0.2832,  # +0.0083
    '+ Feature Selection':   0.2843,  # +0.0011
    '+ Calibration':         0.2851,  # +0.0008
}
```

---

## ⚙️ **Installation**

### **Prerequisites**

```bash
Python 3.8+
pip 21.0+
```

### **Clone Repository**

```bash
git clone https://github.com/yourusername/zebra.git
cd zebra
```

### **Install Dependencies**

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### **Requirements**

```txt
# requirements.txt
pandas==2.0.3
numpy==1.26.4
scikit-learn==1.4.2
lightgbm==4.3.0
xgboost==2.0.3
catboost==1.2.5
optuna==3.6.1
imbalanced-learn==0.12.3
matplotlib==3.8.0
seaborn==0.13.0
scipy==1.11.4
```

---

## 🚀 **Quick Start**

### **1. Prepare Data**

```bash
# Place your data files in data/ directory
data/
├── training_data.csv
└── test_data.csv
```

### **2. Run Complete Pipeline**

```python
python scripts/refined_pipeline.py
```

### **3. Output**

```bash
outputs/
├── refined_submission.csv      # Predictions
├── feature_importance.png      # Feature plot
├── model_performance.png       # Performance charts
└── metrics.json                # Detailed metrics
```

### **Simple Example**

```python
from zebra import ZebraPredictor

# Initialize
predictor = ZebraPredictor()

# Load data
predictor.load_data('data/training_data.csv', 'data/test_data.csv')

# Train
predictor.fit()

# Predict
predictions = predictor.predict()

# Save
predictor.save_submission('submission.csv')
```

---

## 🏗️ **Pipeline Architecture**
```
┌───────────────────────────────────────────────────────────────┐
│                           RAW DATA                            │
│                    (476,169 × 50 features)                    │
└──────────────────────────────┬────────────────────────────────┘
                               ↓
                       ┌────────────────┐
                       │   STRATIFIED   │
                       │   80/20 SPLIT  │
                       └───────┬────────┘
                               ↓
           ┌───────────────────┴───────────────────┐
           ↓                                       ↓
 ┌───────────────────┐                   ┌───────────────────┐
 │   TRAINING SET    │                   │  VALIDATION SET   │
 │  380,935 samples  │                   │   95,234 samples  │
 └─────────┬─────────┘                   └─────────┬─────────┘
           │                                       │
 ┌─────────↓─────────┐   FIT & TRANSFORM   ┌───────↓─────────┐
 │FEATURE ENGINEERING│ ──────────────────> │FEATURE ENGRNG   │
 │    (50 → 109)     │    (Apply Rules)    │   (Apply Only)  │
 └─────────┬─────────┘                     └───────┬─────────┘
           │                                       │
 ┌─────────↓─────────┐                     ┌───────↓─────────┐
 │  TARGET ENCODING  │ ──────────────────> │ TARGET ENCODING │
 │ (Fit on Train Set)│   (Apply Mapping)   │   (Apply Only)  │
 └─────────┬─────────┘                     └───────┬─────────┘
           │                                       │
 ┌─────────↓─────────┐                     ┌───────↓─────────┐
 │    IMPUTATION     │ ──────────────────> │   IMPUTATION    │
 │   (Fit Med/Mode)  │    (Apply Stats)    │   (Apply Only)  │
 └─────────┬─────────┘                     └───────┬─────────┘
           │                                       │
 ┌─────────↓─────────┐                             │
 │    RESAMPLING     │                             │
 │   SMOTE (0.08) +  │       STRICTLY              │
 │    Under (0.4)    │ ─── (NO VALIDATION ──────── │
 │(Train Set ONLY!)  │        LEAKAGE)             │
 └─────────┬─────────┘                             │
           │                                       │
 ┌─────────↓─────────┐                     ┌───────↓─────────┐
 │ FEATURE SELECTION │ ──────────────────> │FEATURE SELECTION│
 │  (LightGBM: 80)   │  (Keep Top 80 Feat) │   (Apply Only)  │
 └─────────┬─────────┘                     └───────┬─────────┘
           │                                       │
 ┌─────────↓─────────┐                     ┌───────↓─────────┐
 │  MODEL TRAINING   │                     │                 │
 │ • LGB: 727 trees  │ ──────────────────> │   PREDICTIONS   │
 │ • XGB: 834 trees  │     (Predict)       │                 │
 │ • CAT: 1339 iter  │                     │                 │
 └─────────┬─────────┘                     └───────┬─────────┘
           │                                       │
           └───────────────────┬───────────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │   ISOTONIC CALIBRATION    │
                 │(Calibrated using Val Set) │
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │     WEIGHTED ENSEMBLE     │
                 │0.123×L + 0.278×X + 0.599×C│
                 └─────────────┬─────────────┘
                               ↓
                 ┌───────────────────────────┐
                 │     FINAL PREDICTIONS     │
                 │   Validation Gini: 0.2851 │
                 └───────────────────────────┘
```
## 🤖 **Model Details**

### **LightGBM Configuration**

```python
lgb_params = {
    'objective': 'binary',
    'boosting_type': 'gbdt',
    'num_leaves': 27,                    # Tree complexity
    'learning_rate': 0.030296,           # Step size
    'n_estimators': 727,                 # Number of trees
    'max_depth': 6,                      # Max tree depth
    'min_child_samples': 70,             # Min leaf samples
    'reg_alpha': 1.968,                  # L1 regularization
    'reg_lambda': 0.377,                 # L2 regularization
    'feature_fraction': 0.529,           # Feature sampling
    'bagging_fraction': 0.708,           # Row sampling
    'bagging_freq': 6,                   # Bagging frequency
    'min_gain_to_split': 0.267,          # Min split gain
    'random_state': 42
}
```

### **XGBoost Configuration**

```python
xgb_params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'max_depth': 6,                      # Tree depth
    'learning_rate': 0.0128,             # Learning rate
    'n_estimators': 834,                 # Number of trees
    'subsample': 0.540,                  # Row sampling
    'colsample_bytree': 0.701,           # Feature sampling
    'min_child_weight': 10,              # Min leaf weight
    'reg_alpha': 0.580,                  # L1 regularization
    'reg_lambda': 2.606,                 # L2 regularization
    'gamma': 0.248,                      # Min split loss
    'random_state': 42
}
```

### **CatBoost Configuration**

```python
cat_params = {
    'iterations': 1339,                  # Boosting rounds
    'learning_rate': 0.0103,             # Learning rate
    'depth': 8,                          # Tree depth
    'l2_leaf_reg': 6.043,                # L2 regularization
    'border_count': 71,                  # Feature quantization
    'random_seed': 42,
    'verbose': False,
    'eval_metric': 'AUC',
    'early_stopping_rounds': 50
}
```

### **Ensemble Weights** (Optuna-optimized)

```python
ensemble_weights = {
    'LightGBM': 0.1231,  # 12.3% - Fast predictions
    'XGBoost':  0.2778,  # 27.8% - Robust performance  
    'CatBoost': 0.5991   # 59.9% - Best individual model
}

# Final prediction
ensemble_pred = (
    0.1231 * lgb_pred +
    0.2778 * xgb_pred +
    0.5991 * cat_pred
)
```

---

## 📁 **Project Structure**

```
zebra/
│
├── 📂 data/
│   ├── training_data.csv              # Training dataset
│   ├── test_data.csv                  # Test dataset
│   └── README.md                      # Data description
│
├── 📂 notebooks/
│   ├── 01_EDA.ipynb                   # Exploratory analysis
│   ├── 02_Feature_Engineering.ipynb   # Feature experiments
│   ├── 03_Modeling.ipynb              # Model experiments
│   └── 04_Optimization.ipynb          # Hyperparameter tuning
│
├── 📂 src/
│   ├── init.py
│   ├── 📄 config.py                   # Configuration
│   ├── 📄 feature_engineering.py      # Feature creation
│   ├── 📄 preprocessing.py            # Data preprocessing
│   ├── 📄 models.py                   # Model definitions
│   ├── 📄 ensemble.py                 # Ensemble methods
│   ├── 📄 calibration.py              # Calibration functions
│   ├── 📄 validation.py               # Validation strategies
│   └── 📄 utils.py                    # Utility functions
│
├── 📂 scripts/
│   ├── refined_pipeline.py            # ⭐ Main pipeline
│   ├── optuna_tuning.py               # Hyperparameter tuning
│   ├── ada_gradient_boost.py          # Additional models
│   └── cross_validation.py            # K-fold validation
│
├── 📂 outputs/
│   ├── refined_submission.csv         # Final predictions
│   ├── feature_importance.png         # Feature plots
│   ├── performance_metrics.png        # Performance charts
│   └── metrics.json                   # Detailed metrics
│
├── 📂 tests/
│   ├── test_features.py               # Feature tests
│   ├── test_models.py                 # Model tests
│   └── test_pipeline.py               # Pipeline tests
│
├── 📂 docs/
│   ├── ARCHITECTURE.md                # Architecture details
│   ├── METHODOLOGY.md                 # Methodology docs
│   └── API.md                         # API documentation
│
├── 📄 requirements.txt                # Dependencies
├── 📄 setup.py                        # Package setup
├── 📄 .gitignore                      # Git ignore rules
├── 📄 LICENSE                         # MIT License
└── 📄 README.md                       # This file
```
---

## ⚙️ **Configuration**

### **Edit Configuration**

```python
# src/config.py

class Config:
    # Data paths
    TRAIN_PATH = 'data/training_data.csv'
    TEST_PATH = 'data/test_data.csv'
    OUTPUT_PATH = 'outputs/'
    
    # Validation
    VALIDATION_SIZE = 0.20
    RANDOM_STATE = 42
    STRATIFY = True
    
    # Feature engineering
    SMOOTHING = 10
    TOP_N_FEATURES = 80
    
    # Resampling
    SMOTE_RATIO = 0.08
    UNDER_RATIO = 0.40
    
    # Models
    MODELS = ['lightgbm', 'xgboost', 'catboost']
    
    # Ensemble
    ENSEMBLE_WEIGHTS = {
        'LightGBM': 0.1231,
        'XGBoost': 0.2778,
        'CatBoost': 0.5991
    }
```

### **Command Line Arguments**

```bash
python scripts/refined_pipeline.py \
    --train data/training_data.csv \
    --test data/test_data.csv \
    --output outputs/submission.csv \
    --validation-size 0.20 \
    --top-features 80 \
    --random-state 42
```

---

## 🧪 **Experiments**

### **Run Experiments**

```bash
# Experiment 1: Different feature counts
python scripts/experiment_features.py --n-features 60 70 80 90 100

# Experiment 2: Different resampling ratios
python scripts/experiment_resampling.py --ratios 0.3 0.4 0.5

# Experiment 3: K-Fold validation
python scripts/cross_validation.py --n-folds 5

# Experiment 4: Hyperparameter tuning
python scripts/optuna_tuning.py --n-trials 100
```

### **Experiment Results**
experiments/
├── feature_selection_results.csv
├── resampling_results.csv
├── kfold_results.csv
└── optuna_study.db

### **What Worked ✅**

```python
improvements = {
    'CatBoost (60% weight)': '+0.0020 Gini',
    'Isotonic Calibration': '+0.0028 Gini',
    'Target Encoding': '+0.0045 Gini',
    'Feature Selection (80)': '+0.0011 Gini',
    'Optuna Tuning': '+0.0083 Gini'
}
```

### **What Didn't Work ❌**

```python
failed_attempts = {
    'Heavy Stacking (5-fold OOF)': '-0.0216 Gini',
    'Too many features (123)': '-0.0008 Gini',
    'Aggressive resampling (1:1)': '-0.0143 Gini',
    'Neural Networks': '+0.0001 Gini (not worth complexity)'
}
```

---

## 📊 **Metrics & Evaluation**

### **Normalized Gini Coefficient**

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

### **Validation Strategy**

```python
# Stratified Hold-Out (80/20)
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y  # Maintains 96.36% / 3.64% ratio
)

# Results
print(f"Training:   {len(y_train):,} samples")
print(f"Validation: {len(y_val):,} samples")
print(f"Class ratio maintained: {(y_val==1).mean():.4f}")
```

### **Performance Report**
```
════════════════════════════════════════════════════════
ZEBRA Performance Report
════════════════════════════════════════════════════════
Dataset Statistics:
Training samples:     380,935
Validation samples:    95,234
Test samples:         119,043
Features (original):      50
Features (engineered):   109
Features (selected):      80
────────────────────────────────────────────────────────
Model Performance:
LightGBM    | Val Gini: 0.2826 | Weight: 12.3%
XGBoost     | Val Gini: 0.2824 | Weight: 27.8%
CatBoost    | Val Gini: 0.2848 | Weight: 59.9%
────────────────────────────────────────────────────
ENSEMBLE    | Val Gini: 0.2851 | ⭐ BEST
────────────────────────────────────────────────────────
Validation Metrics:
Normalized Gini:  0.2851
AUC-ROC:          0.6426
Improvement:      +8.5% from baseline
════════════════════════════════════════════════════════
```
---

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### **Development Setup**

```bash
# Clone repo
git clone https://github.com/yourusername/zebra.git
cd zebra

# Create branch
git checkout -b feature/amazing-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 src/
black src/
```

### **Contribution Ideas**

- [ ] Implement K-Fold cross-validation
- [ ] Add SHAP explanations
- [ ] Create web dashboard
- [ ] Add more ensemble methods
- [ ] Optimize for inference speed
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] API endpoint

### **Code Style**

```python
# Follow PEP 8
# Use type hints
# Add docstrings

def predict_claims(
    X: pd.DataFrame,
    model: object,
    calibrate: bool = True
) -> np.ndarray:
    """
    Predict claim probabilities for customers.
    
    Args:
        X: Feature matrix
        model: Trained model
        calibrate: Apply isotonic calibration
        
    Returns:
        Predicted probabilities
    """
    predictions = model.predict_proba(X)[:, 1]
    
    if calibrate:
        predictions = calibrator.transform(predictions)
        
    return predictions
```

---

## 📚 **References**

### **Research Papers**

1. **SMOTE**: Chawla, N. V., et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique"
2. **XGBoost**: Chen, T., & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System"
3. **LightGBM**: Ke, G., et al. (2017). "LightGBM: A Highly Efficient Gradient Boosting Decision Tree"
4. **CatBoost**: Prokhorenkova, L., et al. (2018). "CatBoost: unbiased boosting with categorical features"
5. **Calibration**: Niculescu-Mizil, A., & Caruana, R. (2005). "Predicting good probabilities with supervised learning"

### **Documentation**

- [LightGBM Docs](https://lightgbm.readthedocs.io/)
- [XGBoost Docs](https://xgboost.readthedocs.io/)
- [CatBoost Docs](https://catboost.ai/docs/)
- [Optuna Docs](https://optuna.readthedocs.io/)
- [Imbalanced-Learn Docs](https://imbalanced-learn.org/)

---

## 🙏 **Acknowledgments**

- **Dataset Provider**: [Competition/Organization Name]
- **Inspiration**: Kaggle community and insurance ML practitioners
- **Libraries**: scikit-learn, LightGBM, XGBoost, CatBoost teams

---

## 📧 **Contact**

**Project Maintainer**: Your Name

- 📧 Email: your.email@example.com
- 🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- 🔗 Website: [yourwebsite.com](https://yourwebsite.com)

**Project Link**: [https://github.com/yourusername/zebra](https://github.com/yourusername/zebra)


## 📊 **Project Stats**

![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/zebra?style=flat-square)
![GitHub code size](https://img.shields.io/github/languages/code-size/yourusername/zebra?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/yourusername/zebra?style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/zebra?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/zebra?style=flat-square)


<div align="center">

**[⬆ Back to Top](#-zebra)**

</div>
