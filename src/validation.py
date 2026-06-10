import numpy as np
from sklearn.metrics import make_scorer

def gini(y_true, y_pred):
    """Calculate Gini coefficient."""
    # Handle pandas Series/DataFrames by converting to numpy arrays
    if hasattr(y_true, 'values'):
        y_true = y_true.values
        
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    # Sort by predicted probabilities
    sorted_indices = np.argsort(y_pred)
    sorted_y_true = y_true[sorted_indices]

    # Calculate cumulative values
    cumulative_true = np.cumsum(sorted_y_true)
    cumulative_index = np.arange(1, len(y_true) + 1)

    # Calculate Gini
    gini_val = (np.sum((cumulative_index - cumulative_true)) /
                (np.sum(cumulative_index) - np.sum(cumulative_true)))

    return gini_val

def normalized_gini(y_true, y_pred):
    """Calculate Normalized Gini coefficient."""
    return gini(y_true, y_pred) / gini(y_true, y_true)

# Custom scorer for scikit-learn
gini_scorer = make_scorer(normalized_gini, needs_proba=True)
