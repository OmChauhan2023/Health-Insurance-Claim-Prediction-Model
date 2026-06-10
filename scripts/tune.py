import sys
from pathlib import Path
import optuna
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data, split_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraCategoricalEncoder, apply_resampling
from sklearn.pipeline import Pipeline
from src.validation import normalized_gini

def objective(trial, X_train, y_train, X_val, y_val):
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt',
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 15, 63),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'min_child_samples': trial.suggest_int('min_child_samples', 10, 100),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.5, 1.0),
        'bagging_fraction': trial.suggest_float('bagging_fraction', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-3, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-3, 10.0, log=True),
        'random_state': 42,
        'verbose': -1
    }
    
    model = lgb.LGBMClassifier(**params, n_estimators=200)
    model.fit(X_train, y_train)
    
    preds = model.predict_proba(X_val)[:, 1]
    return normalized_gini(y_val, preds)

def main():
    print("="*60)
    print("ZEBRA HYPERPARAMETER TUNING (LightGBM)")
    print("="*60)
    
    config = load_config()
    train_path = project_root / config['data']['train_path']
    target_col = config['features']['target']
    
    # 1. Load Data
    train_df, _ = load_data(train_path)
    X_train_raw, X_val_raw, y_train, y_val = split_data(train_df, target_col)
    
    # 2. Preprocess Data
    print("\nPreprocessing data for tuning...")
    preprocessor = Pipeline([
        ('feat_eng', ZebraFeatureEngineer()),
        ('imputer', ZebraImputer(
            config['features']['binary'],
            config['features']['categorical'],
            config['features']['numeric']
        )),
        ('encoder', ZebraCategoricalEncoder(config['features']['categorical']))
    ])
    
    X_train_proc = preprocessor.fit_transform(X_train_raw)
    X_val_proc = preprocessor.transform(X_val_raw)
    
    X_train_res, y_train_res = apply_resampling(
        X_train_proc, y_train, 
        config['preprocessing']['smote_ratio'], 
        config['preprocessing']['under_ratio']
    )
    
    # 3. Tuning
    print("\nStarting Optuna Study...")
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda t: objective(t, X_train_res, y_train_res, X_val_proc, y_val), n_trials=20)
    
    print("\n" + "="*60)
    print("Best Trial:")
    print(f"  Gini Score: {study.best_value:.4f}")
    print("  Params:")
    for key, value in study.best_trial.params.items():
        print(f"    {key}: {value}")
    print("="*60)

if __name__ == "__main__":
    main()
