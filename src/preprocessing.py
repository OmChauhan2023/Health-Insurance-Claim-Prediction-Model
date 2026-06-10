import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

class ZebraImputer(BaseEstimator, TransformerMixin):
    """
    Custom imputer following the specific rules of the original monolithic script:
    - Binary features: Mode (0 or 1)
    - Categorical features: Mode
    - Numeric features: Median
    - Fallback: Median for numeric/float, Mode for others.
    """
    def __init__(self, binary_features, categorical_features, numeric_features):
        self.binary_features = binary_features
        self.categorical_features = categorical_features
        self.numeric_features = numeric_features
        self.fill_values = {}
        
    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        
        # Determine fill values for binary
        for feat in self.binary_features:
            if feat in X_df.columns:
                self.fill_values[feat] = X_df[feat].mode()[0] if not X_df[feat].mode().empty else 0
                
        # Determine fill values for categorical
        for feat in self.categorical_features:
            if feat in X_df.columns:
                self.fill_values[feat] = X_df[feat].mode()[0] if not X_df[feat].mode().empty else -1
                
        # Determine fill values for numeric
        for feat in self.numeric_features:
            if feat in X_df.columns:
                self.fill_values[feat] = X_df[feat].median()
                
        # Fallback for engineered or unlisted features
        for col in X_df.columns:
            if col not in self.fill_values:
                if X_df[col].dtype in ['float64', 'int64']:
                    self.fill_values[col] = X_df[col].median()
                else:
                    self.fill_values[col] = X_df[col].mode()[0] if not X_df[col].mode().empty else 0
                    
        return self
        
    def transform(self, X, y=None):
        X_new = pd.DataFrame(X).copy()
        for col, fill_val in self.fill_values.items():
            if col in X_new.columns:
                X_new[col] = X_new[col].fillna(fill_val)
        return X_new


class ZebraCategoricalEncoder(BaseEstimator, TransformerMixin):
    """
    Applies LabelEncoding to categorical columns identically to the original script.
    """
    def __init__(self, categorical_features):
        self.categorical_features = categorical_features
        self.encoders = {}
        
    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        for feat in self.categorical_features:
            if feat in X_df.columns:
                le = LabelEncoder()
                # Fit on string representation as in original script
                le.fit(X_df[feat].astype(str))
                self.encoders[feat] = le
        return self
        
    def transform(self, X, y=None):
        X_new = pd.DataFrame(X).copy()
        for feat, le in self.encoders.items():
            if feat in X_new.columns:
                # Use a mapping approach to handle unseen categories gracefully
                # If a category is unseen, map it to an unknown/default class
                classes = dict(zip(le.classes_, le.transform(le.classes_)))
                X_new[feat] = X_new[feat].astype(str).map(classes).fillna(-1).astype(int)
        return X_new

def apply_resampling(X, y, smote_ratio=0.1, under_ratio=0.3, random_state=42):
    """
    Applies SMOTE + Random Under Sampling.
    """
    print(f"Applying SMOTE (ratio={smote_ratio}) and UnderSampling (ratio={under_ratio})...")
    smote = SMOTE(sampling_strategy=smote_ratio, random_state=random_state)
    under = RandomUnderSampler(sampling_strategy=under_ratio, random_state=random_state)
    
    X_res, y_res = smote.fit_resample(X, y)
    X_res, y_res = under.fit_resample(X_res, y_res)
    
    print(f"Resampled dataset shape: {X_res.shape}")
    return X_res, y_res
