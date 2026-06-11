"""
ZEBRA Hyperparameter Tuning Script
Runs Optuna to find the best hyperparameters for LightGBM, XGBoost, and CatBoost.
"""
import sys
from pathlib import Path
import optuna
import joblib
import pandas as pd
import numpy as np

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data, split_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraTargetEncoder, ZebraFeatureSelector, apply_resampling
from src.validation import normalized_gini
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier

def load_and_preprocess():
    config = load_config()
    train_path = project_root / config['data']['train_path']
    target_col = config['features']['target']
    random_state = config['preprocessing']['random_state']

    print("Loading data...")
    train_df, _ = load_data(train_path)
    X_train_raw, X_val_raw, y_train, y_val = split_data(train_df, target_col, test_size=0.2, random_state=random_state)

    print("Engineering features...")
    feat_eng = ZebraFeatureEngineer()
    X_train_eng = feat_eng.fit_transform(X_train_raw)
    X_val_eng = feat_eng.transform(X_val_raw)

    print("Imputing...")
    imputer = ZebraImputer(config['features']['binary'], config['features']['categorical'], config['features']['numeric'])
    X_train_imp = imputer.fit_transform(X_train_eng)
    X_val_imp = imputer.transform(X_val_eng)

    print("Target Encoding...")
    encoder = ZebraTargetEncoder(config['features']['categorical'], smoothing=10)
    X_train_enc = encoder.fit_transform(X_train_imp, y_train)
    X_val_enc = encoder.transform(X_val_imp)

    print("Resampling...")
    X_train_res, y_train_res = apply_resampling(X_train_enc, y_train, 
                                                smote_ratio=config['preprocessing']['smote_ratio'], 
                                                under_ratio=config['preprocessing']['under_ratio'], 
                                                random_state=random_state)

    print("Feature Selection...")
    selector = ZebraFeatureSelector(keep_percentile=0.65, random_state=random_state)
    X_train_sel = selector.fit_transform(X_train_res, y_train_res)
    X_val_sel = selector.transform(X_val_enc)

    return X_train_sel, y_train_res, X_val_sel, y_val

def tune_lightgbm(X_train, y_train, X_val, y_val, n_trials=500):
    def objective(trial):
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'num_leaves': trial.suggest_int('num_leaves', 20, 150),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 300, 1500),
            'max_depth': trial.suggest_int('max_depth', 4, 10),
            'min_child_samples': trial.suggest_int('min_child_samples', 20, 150),
            'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
            'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True),
            'feature_fraction': trial.suggest_float('feature_fraction', 0.4, 1.0),
            'bagging_fraction': trial.suggest_float('bagging_fraction', 0.4, 1.0),
            'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
            'min_gain_to_split': trial.suggest_float('min_gain_to_split', 0, 1),
            'random_state': 42,
            'verbose': -1
        }
        model = lgb.LGBMClassifier(**params)
        model.fit(X_train, y_train)
        preds = model.predict_proba(X_val)[:, 1]
        return normalized_gini(y_val, preds)

    study = optuna.create_study(direction='maximize')
    
    # WARM START: Enqueue previous best parameters
    try:
        import json
        with open("outputs/best_lgb_params.json", "r") as f:
            best_params = json.load(f)
        study.enqueue_trial(best_params)
        print("Warm-starting LightGBM with previous best parameters.")
    except Exception as e:
        print("Could not load previous LightGBM params for warm start.")

    study.optimize(objective, n_trials=n_trials)
    print("Best LightGBM params:", study.best_trial.params)
    return study.best_trial.params

def tune_xgboost(X_train, y_train, X_val, y_val, n_trials=500):
    def objective(trial):
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'auc',
            'max_depth': trial.suggest_int('max_depth', 4, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 300, 1500),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 20),
            'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
            'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True),
            'gamma': trial.suggest_float('gamma', 0, 1.0),
            'random_state': 42,
            'tree_method': 'hist'
        }
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)
        preds = model.predict_proba(X_val)[:, 1]
        return normalized_gini(y_val, preds)

    study = optuna.create_study(direction='maximize')
    
    # WARM START: Enqueue previous best parameters
    try:
        import json
        with open("outputs/best_xgb_params.json", "r") as f:
            best_params = json.load(f)
        study.enqueue_trial(best_params)
        print("Warm-starting XGBoost with previous best parameters.")
    except Exception as e:
        print("Could not load previous XGBoost params for warm start.")

    study.optimize(objective, n_trials=n_trials)
    print("Best XGBoost params:", study.best_trial.params)
    return study.best_trial.params

def tune_catboost(X_train, y_train, X_val, y_val, n_trials=500):
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 300, 1500),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
            'depth': trial.suggest_int('depth', 4, 10),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1.0, 10.0),
            'border_count': trial.suggest_int('border_count', 32, 255),
            'random_seed': 42,
            'verbose': False,
            'eval_metric': 'AUC',
            'early_stopping_rounds': 50
        }
        model = CatBoostClassifier(**params)
        model.fit(X_train, y_train, eval_set=(X_val, y_val), verbose=False)
        preds = model.predict_proba(X_val)[:, 1]
        return normalized_gini(y_val, preds)

    study = optuna.create_study(direction='maximize')
    
    # WARM START: Enqueue previous best parameters
    try:
        import json
        with open("outputs/best_cat_params.json", "r") as f:
            best_params = json.load(f)
        study.enqueue_trial(best_params)
        print("Warm-starting CatBoost with previous best parameters.")
    except Exception as e:
        print("Could not load previous CatBoost params for warm start.")

    study.optimize(objective, n_trials=n_trials)
    print("Best CatBoost params:", study.best_trial.params)
    return study.best_trial.params

def main():
    print("Starting Hyperparameter Tuning...")
    X_train, y_train, X_val, y_val = load_and_preprocess()
    
    print("\n--- Tuning LightGBM ---")
    lgb_params = tune_lightgbm(X_train, y_train, X_val, y_val, n_trials=50)
    
    print("\n--- Tuning XGBoost ---")
    xgb_params = tune_xgboost(X_train, y_train, X_val, y_val, n_trials=50)
    
    print("\n--- Tuning CatBoost ---")
    cat_params = tune_catboost(X_train, y_train, X_val, y_val, n_trials=50)
    
    import json
    with open("outputs/best_lgb_params.json", "w") as f:
        json.dump(lgb_params, f)
    with open("outputs/best_xgb_params.json", "w") as f:
        json.dump(xgb_params, f)
    with open("outputs/best_cat_params.json", "w") as f:
        json.dump(cat_params, f)

    print("\nTuning Complete!")
    print("Update `src/models.py` with these parameters.")

if __name__ == "__main__":
    main()
