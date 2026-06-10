import numpy as np
from sklearn.metrics import make_scorer, roc_auc_score

def normalized_gini(y_true, y_pred):
    """
    Calculate Normalized Gini Coefficient.
    
    Uses the standard relationship: Gini = 2 * AUC - 1
    This is the industry-standard formula used in insurance risk modeling.
    
    Range: [-1, 1]
    - 1.0: Perfect ranking
    - 0.0: Random model
    - <0: Worse than random
    """
    if hasattr(y_true, 'values'):
        y_true = y_true.values
    return 2 * roc_auc_score(y_true, y_pred) - 1

# Custom scorer for scikit-learn
gini_scorer = make_scorer(normalized_gini, needs_proba=True)
