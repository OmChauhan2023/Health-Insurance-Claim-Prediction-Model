import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ZebraFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Scikit-Learn compatible transformer for creating new features.
    Expands the original 50 features to ~109 through:
    - Missing value indicators
    - Interaction features (multiplicative)
    - Ratio features
    - Polynomial features
    - Aggregation features (sum, mean of binary/numeric groups)
    """
    def __init__(self):
        self.high_missing_features = ['feature_39', 'feature_8', 'feature_45', 'feature_38']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_new = X.copy()

        # 1. Missing value indicators
        for feat in self.high_missing_features:
            if feat in X_new.columns:
                X_new[f'{feat}_missing'] = X_new[feat].isnull().astype(int)

        # 2. Core interaction features (multiplicative)
        pairs = [
            ('feature_24', 'feature_29'),
            ('feature_10', 'feature_16'),
            ('feature_22', 'feature_23'),
            ('feature_24', 'feature_33'),
            ('feature_29', 'feature_33'),
            ('feature_10', 'feature_24'),
            ('feature_16', 'feature_22'),
            ('feature_29', 'feature_45'),
            ('feature_24', 'feature_45'),
        ]
        for f1, f2 in pairs:
            if f1 in X_new.columns and f2 in X_new.columns:
                X_new[f'{f1}_{f2}_interact'] = X_new[f1] * X_new[f2]

        # 3. Ratio features
        ratio_pairs = [
            ('feature_10', 'feature_33'),
            ('feature_24', 'feature_33'),
            ('feature_29', 'feature_10'),
            ('feature_45', 'feature_33'),
        ]
        for num, den in ratio_pairs:
            if num in X_new.columns and den in X_new.columns:
                X_new[f'{num}_{den}_ratio'] = X_new[num] / (X_new[den] + 1e-5)

        # 4. Polynomial features (squared) for top correlated features
        poly_features = [
            'feature_24', 'feature_29', 'feature_33',
            'feature_10', 'feature_45', 'feature_13',
            'feature_25', 'feature_37', 'feature_40'
        ]
        for feat in poly_features:
            if feat in X_new.columns:
                X_new[f'{feat}_sq'] = X_new[feat] ** 2

        # 5. Log transforms (for skewed features with positive values)
        log_features = ['feature_25', 'feature_33', 'feature_37', 'feature_40', 'feature_13']
        for feat in log_features:
            if feat in X_new.columns:
                X_new[f'{feat}_log'] = np.log1p(X_new[feat].clip(lower=0))

        # 6. Sum of binary features
        binary_cols = [c for c in X_new.columns if c.startswith('feature_') and X_new[c].nunique() <= 2]
        if binary_cols:
            X_new['binary_sum'] = X_new[binary_cols].sum(axis=1)

        # 7. Mean and std of numeric feature groups
        numeric_core = [f'feature_{i}' for i in [9, 10, 13, 17, 24, 26, 29, 33, 36, 37, 40, 43, 47, 48, 50] if f'feature_{i}' in X_new.columns]
        if numeric_core:
            X_new['numeric_mean'] = X_new[numeric_core].mean(axis=1)
            X_new['numeric_std'] = X_new[numeric_core].std(axis=1)
            X_new['numeric_max'] = X_new[numeric_core].max(axis=1)
            X_new['numeric_min'] = X_new[numeric_core].min(axis=1)

        # 8. Count of missing values per row (across all original features)
        X_new['missing_count'] = X_new[[c for c in X_new.columns if c.startswith('feature_')]].isnull().sum(axis=1)

        return X_new
