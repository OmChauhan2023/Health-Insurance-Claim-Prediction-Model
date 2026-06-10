import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler


class ZebraImputer(BaseEstimator, TransformerMixin):
    """
    Custom imputer:
    - Binary features: Mode
    - Categorical features: Mode
    - Numeric features: Median
    """
    def __init__(self, binary_features, categorical_features, numeric_features):
        self.binary_features = binary_features
        self.categorical_features = categorical_features
        self.numeric_features = numeric_features
        self.fill_values = {}

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        for feat in self.binary_features:
            if feat in X_df.columns:
                self.fill_values[feat] = X_df[feat].mode()[0] if not X_df[feat].mode().empty else 0
        for feat in self.categorical_features:
            if feat in X_df.columns:
                self.fill_values[feat] = X_df[feat].mode()[0] if not X_df[feat].mode().empty else -1
        for feat in self.numeric_features:
            if feat in X_df.columns:
                self.fill_values[feat] = X_df[feat].median()
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


class ZebraTargetEncoder(BaseEstimator, TransformerMixin):
    """
    Target Encoding with smoothing to prevent overfitting.
    Replaces LabelEncoder for categorical features.
    smoothing=10 controls the regularization strength.
    """
    def __init__(self, categorical_features, smoothing=10):
        self.categorical_features = categorical_features
        self.smoothing = smoothing
        self.encoding_map = {}
        self.global_mean = None

    def fit(self, X, y):
        X_df = pd.DataFrame(X).copy()
        y_arr = np.asarray(y) if hasattr(y, 'values') else np.asarray(y)

        self.global_mean = y_arr.mean()

        temp_df = X_df.copy()
        temp_df['__target__'] = y_arr

        for feat in self.categorical_features:
            if feat not in temp_df.columns:
                continue
            stats = temp_df.groupby(feat)['__target__'].agg(['mean', 'count'])
            # Smoothed target encoding formula
            smoother = stats['count'] / (stats['count'] + self.smoothing)
            self.encoding_map[feat] = (
                smoother * stats['mean'] + (1 - smoother) * self.global_mean
            ).to_dict()
        return self

    def transform(self, X, y=None):
        X_new = pd.DataFrame(X).copy()
        for feat, mapping in self.encoding_map.items():
            if feat in X_new.columns:
                X_new[feat] = X_new[feat].map(mapping).fillna(self.global_mean)
        return X_new


class ZebraFeatureSelector(BaseEstimator, TransformerMixin):
    """
    Selects top N features by LightGBM feature importance.
    Fit on training data, apply same mask to validation/test.
    """
    def __init__(self, n_features=80, random_state=42):
        self.n_features = n_features
        self.random_state = random_state
        self.selected_features = None

    def fit(self, X, y):
        import lightgbm as lgb
        X_df = pd.DataFrame(X)
        selector_model = lgb.LGBMClassifier(
            n_estimators=100,
            random_state=self.random_state,
            verbose=-1
        )
        selector_model.fit(X_df, y)
        importance = pd.Series(
            selector_model.feature_importances_,
            index=X_df.columns
        ).sort_values(ascending=False)
        self.selected_features = importance.head(self.n_features).index.tolist()
        print(f"Selected top {len(self.selected_features)} features.")
        return self

    def transform(self, X, y=None):
        X_df = pd.DataFrame(X)
        return X_df[self.selected_features]


def apply_resampling(X, y, smote_ratio=0.08, under_ratio=0.4, random_state=42):
    """
    Applies SMOTE + Random Under Sampling.
    Default ratios match the original ZEBRA pipeline (0.08/0.4).
    """
    print(f"Applying SMOTE (ratio={smote_ratio}) and UnderSampling (ratio={under_ratio})...")
    smote = SMOTE(sampling_strategy=smote_ratio, random_state=random_state)
    under = RandomUnderSampler(sampling_strategy=under_ratio, random_state=random_state)
    X_res, y_res = smote.fit_resample(X, y)
    X_res, y_res = under.fit_resample(X_res, y_res)
    print(f"Resampled dataset shape: {X_res.shape}")
    return X_res, y_res
