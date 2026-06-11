"""
Temporary script to test user-provided hyperparameters and ensemble weights.
Runs side-by-side without interfering with Optuna.
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraTargetEncoder, ZebraFeatureSelector, apply_resampling
from src.validation import normalized_gini

import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier

def get_models(random_state=42):
    lgb_params = {
        'objective': 'binary',
        'boosting_type': 'gbdt',
        'num_leaves': 27,
        'learning_rate': 0.030296,
        'n_estimators': 727,
        'max_depth': 6,
        'min_child_samples': 70,
        'reg_alpha': 1.968,
        'reg_lambda': 0.377,
        'feature_fraction': 0.529,
        'bagging_fraction': 0.708,
        'bagging_freq': 6,
        'min_gain_to_split': 0.267,
        'random_state': random_state,
        'verbose': -1
    }
    xgb_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 6,
        'learning_rate': 0.0128,
        'n_estimators': 834,
        'subsample': 0.540,
        'colsample_bytree': 0.701,
        'min_child_weight': 10,
        'reg_alpha': 0.580,
        'reg_lambda': 2.606,
        'gamma': 0.248,
        'random_state': random_state,
        'tree_method': 'hist'
    }
    cat_params = {
        'iterations': 1339,
        'learning_rate': 0.0103,
        'depth': 8,
        'l2_leaf_reg': 6.043,
        'border_count': 71,
        'random_seed': random_state,
        'verbose': False,
        'eval_metric': 'AUC',
        'early_stopping_rounds': 50
    }
    return {
        'LightGBM': lgb.LGBMClassifier(**lgb_params),
        'XGBoost': xgb.XGBClassifier(**xgb_params),
        'CatBoost': CatBoostClassifier(**cat_params)
    }

def main():
    print("=" * 60)
    print("Testing User-Provided Hyperparameters & Weights")
    print("=" * 60)

    config = load_config()
    train_path = project_root / config['data']['train_path']
    target_col = config['features']['target']
    random_state = config['preprocessing']['random_state']
    n_folds = 5

    print("Loading data...")
    train_df, _ = load_data(train_path)
    y_all = train_df[target_col]
    X_all_raw = train_df.drop(columns=[target_col, 'id'])

    print("Engineering features...")
    feat_eng = ZebraFeatureEngineer()
    X_all_eng = feat_eng.fit_transform(X_all_raw)

    print("Imputing...")
    imputer = ZebraImputer(
        config['features']['binary'],
        config['features']['categorical'],
        config['features']['numeric']
    )
    X_all_imp = imputer.fit_transform(X_all_eng)

    print("5-Fold CV (OOF Encoding + Resampling + Training)...")
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    
    model_names = ['LightGBM', 'XGBoost', 'CatBoost']
    oof_preds = {name: np.zeros(len(X_all_imp)) for name in model_names}
    y_all_arr = y_all.values

    for fold, (train_idx, val_idx) in enumerate(skf.split(X_all_imp, y_all_arr), 1):
        print(f"\n--- Fold {fold}/{n_folds} ---")
        X_tr_fold = X_all_imp.iloc[train_idx].copy()
        y_tr_fold = y_all_arr[train_idx]
        X_val_fold = X_all_imp.iloc[val_idx].copy()

        # OOF Target Encoding
        encoder = ZebraTargetEncoder(config['features']['categorical'], smoothing=10)
        X_tr_enc = encoder.fit_transform(X_tr_fold, y_tr_fold)
        X_val_enc = encoder.transform(X_val_fold)

        # Resampling
        X_tr_res, y_tr_res = apply_resampling(
            X_tr_enc, y_tr_fold,
            smote_ratio=config['preprocessing']['smote_ratio'],
            under_ratio=config['preprocessing']['under_ratio'],
            random_state=random_state
        )

        # Feature Selection
        selector = ZebraFeatureSelector(n_features=80, random_state=random_state)
        X_tr_sel = selector.fit_transform(X_tr_res, y_tr_res)
        X_val_sel = selector.transform(X_val_enc)

        # Train Models
        models = get_models(random_state=random_state)
        for name, model in models.items():
            if name == 'CatBoost':
                from sklearn.model_selection import train_test_split
                X_t, X_e, y_t, y_e = train_test_split(X_tr_sel, y_tr_res, test_size=0.1, random_state=random_state)
                model.fit(X_t, y_t, eval_set=(X_e, y_e))
            else:
                model.fit(X_tr_sel, y_tr_res)
            
            oof_preds[name][val_idx] = model.predict_proba(X_val_sel)[:, 1]

    print("\n--- Model OOF Gini Scores ---")
    for name in model_names:
        gini = normalized_gini(y_all_arr, oof_preds[name])
        print(f"{name:10}: {gini:.4f}")

    print("\n--- Applying User Ensemble Weights ---")
    w_lgb = 0.1231
    w_xgb = 0.2778
    w_cat = 0.5991
    
    ensemble_oof = (w_lgb * oof_preds['LightGBM'] +
                    w_xgb * oof_preds['XGBoost'] +
                    w_cat * oof_preds['CatBoost'])
    
    final_gini = normalized_gini(y_all_arr, ensemble_oof)
    print(f"FINAL WEIGHTED OOF GINI: {final_gini:.4f}")

if __name__ == "__main__":
    main()
