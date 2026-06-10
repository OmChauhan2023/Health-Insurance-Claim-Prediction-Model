import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class ZebraFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Scikit-Learn compatible transformer for creating new features.
    Matches the logic originally found in the monolithic script.
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
                
        # 2. Interaction features
        if 'feature_24' in X_new.columns and 'feature_29' in X_new.columns:
            X_new['feat_24_29_interaction'] = X_new['feature_24'] * X_new['feature_29']
            
        if 'feature_10' in X_new.columns and 'feature_16' in X_new.columns:
            X_new['feat_10_16_interaction'] = X_new['feature_10'] * X_new['feature_16']
            
        if 'feature_22' in X_new.columns and 'feature_23' in X_new.columns:
            X_new['feat_22_23_interaction'] = X_new['feature_22'] * X_new['feature_23']
            
        # 3. Ratio features
        if 'feature_10' in X_new.columns and 'feature_33' in X_new.columns:
            X_new['feat_10_33_ratio'] = X_new['feature_10'] / (X_new['feature_33'] + 1e-5)
            
        # 4. Polynomial features
        if 'feature_24' in X_new.columns:
            X_new['feature_24_squared'] = X_new['feature_24'] ** 2
            
        if 'feature_29' in X_new.columns:
            X_new['feature_29_squared'] = X_new['feature_29'] ** 2
            
        # 5. Sum of binary features
        binary_cols = [col for col in X_new.columns if col.startswith('feature_') and X_new[col].nunique() <= 2]
        if len(binary_cols) > 0:
            X_new['binary_sum'] = X_new[binary_cols].sum(axis=1)
            
        # 6. Count of missing values per row
        X_new['missing_count'] = X_new.isnull().sum(axis=1)
        
        return X_new
