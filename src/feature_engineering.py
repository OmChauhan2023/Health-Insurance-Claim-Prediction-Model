import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ZebraFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Comprehensive feature engineering to expand 50 raw features to ~109.
    Covers: missingness indicators, interactions, ratios, polynomials,
    log transforms, aggregations, and binning.
    """
    def __init__(self):
        self.high_missing_features = ['feature_39', 'feature_8', 'feature_45', 'feature_38']

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_new = X.copy()

        # === 1. Missing value indicators (4 features) ===
        for feat in self.high_missing_features:
            if feat in X_new.columns:
                X_new[f'{feat}_missing'] = X_new[feat].isnull().astype(int)

        # === 2. Pairwise interaction features (15 features) ===
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
            ('feature_33', 'feature_45'),
            ('feature_10', 'feature_45'),
            ('feature_13', 'feature_24'),
            ('feature_25', 'feature_33'),
            ('feature_37', 'feature_24'),
            ('feature_40', 'feature_24'),
        ]
        for f1, f2 in pairs:
            if f1 in X_new.columns and f2 in X_new.columns:
                X_new[f'{f1}_{f2}_interact'] = X_new[f1] * X_new[f2]

        # === 3. Ratio features (6 features) ===
        ratio_pairs = [
            ('feature_10', 'feature_33'),
            ('feature_24', 'feature_33'),
            ('feature_29', 'feature_10'),
            ('feature_45', 'feature_33'),
            ('feature_13', 'feature_37'),
            ('feature_25', 'feature_40'),
        ]
        for num, den in ratio_pairs:
            if num in X_new.columns and den in X_new.columns:
                X_new[f'{num}_{den}_ratio'] = X_new[num] / (X_new[den].abs() + 1e-5)

        # === 4. Polynomial (squared) features (12 features) ===
        poly_features = [
            'feature_24', 'feature_29', 'feature_33',
            'feature_10', 'feature_45', 'feature_13',
            'feature_25', 'feature_37', 'feature_40',
            'feature_9', 'feature_26', 'feature_47'
        ]
        for feat in poly_features:
            if feat in X_new.columns:
                X_new[f'{feat}_sq'] = X_new[feat] ** 2

        # === 5. Log transforms (8 features) ===
        log_features = [
            'feature_25', 'feature_33', 'feature_37',
            'feature_40', 'feature_13', 'feature_9',
            'feature_47', 'feature_48'
        ]
        for feat in log_features:
            if feat in X_new.columns:
                X_new[f'{feat}_log'] = np.log1p(X_new[feat].clip(lower=0))

        # === 6. Aggregation features across numeric groups (6 features) ===
        numeric_core = [f'feature_{i}' for i in [9, 10, 13, 17, 24, 26, 29, 33, 36, 37, 40, 43, 47, 48, 50]
                        if f'feature_{i}' in X_new.columns]
        if numeric_core:
            X_new['numeric_mean'] = X_new[numeric_core].mean(axis=1)
            X_new['numeric_std']  = X_new[numeric_core].std(axis=1)
            X_new['numeric_max']  = X_new[numeric_core].max(axis=1)
            X_new['numeric_min']  = X_new[numeric_core].min(axis=1)
            X_new['numeric_range']= X_new['numeric_max'] - X_new['numeric_min']
            X_new['numeric_sum']  = X_new[numeric_core].sum(axis=1)

        # === 7. Binary feature aggregations (3 features) ===
        binary_cols = [c for c in X_new.columns if c.startswith('feature_') and X_new[c].nunique() <= 2]
        if binary_cols:
            X_new['binary_sum']  = X_new[binary_cols].sum(axis=1)
            X_new['binary_mean'] = X_new[binary_cols].mean(axis=1)
            X_new['binary_count_zero'] = (X_new[binary_cols] == 0).sum(axis=1)

        # === 8. Row-level missing count (1 feature) ===
        orig_feat_cols = [c for c in X_new.columns if c.startswith('feature_') and '_' not in c.replace('feature_', '')]
        X_new['missing_count'] = X_new[[c for c in orig_feat_cols if c in X_new.columns]].isnull().sum(axis=1)

        # === 9. Difference features (4 features) ===
        diff_pairs = [
            ('feature_24', 'feature_29'),
            ('feature_33', 'feature_45'),
            ('feature_10', 'feature_33'),
            ('feature_37', 'feature_13'),
        ]
        for f1, f2 in diff_pairs:
            if f1 in X_new.columns and f2 in X_new.columns:
                X_new[f'{f1}_{f2}_diff'] = X_new[f1] - X_new[f2]

        # === 10. Automated Feature Engineering (PolynomialFeatures) ===
        if numeric_core:
            from sklearn.preprocessing import PolynomialFeatures
            # Fill NaNs temporarily for PolyFeatures
            X_poly_temp = X_new[numeric_core].fillna(0)
            poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
            poly_features = poly.fit_transform(X_poly_temp)
            # Skip the original features (degree 1) which are first len(numeric_core) columns
            n_orig = len(numeric_core)
            poly_interactions = poly_features[:, n_orig:]
            feature_names = poly.get_feature_names_out(numeric_core)[n_orig:]
            
            # Clean up names
            feature_names = [name.replace(' ', '_interact_') for name in feature_names]
            
            # Create a DataFrame and concat it
            poly_df = pd.DataFrame(poly_interactions, columns=feature_names, index=X_new.index)
            X_new = pd.concat([X_new, poly_df], axis=1)

        # === 11. Expanded GroupBy Statistical Features ===
        cat_groupers = ['feature_3', 'feature_7', 'feature_8', 'feature_12']
        num_targets = ['feature_10', 'feature_24', 'feature_16', 'feature_18']
        for cat in cat_groupers:
            if cat in X_new.columns:
                for num in num_targets:
                    if num in X_new.columns:
                        group_mean = X_new.groupby(cat)[num].transform('mean')
                        group_std = X_new.groupby(cat)[num].transform('std').fillna(0)
                        group_min = X_new.groupby(cat)[num].transform('min')
                        group_max = X_new.groupby(cat)[num].transform('max')
                        
                        X_new[f'{num}_groupby_{cat}_mean'] = group_mean
                        X_new[f'{num}_groupby_{cat}_std'] = group_std
                        X_new[f'{num}_groupby_{cat}_min'] = group_min
                        X_new[f'{num}_groupby_{cat}_max'] = group_max

        return X_new
