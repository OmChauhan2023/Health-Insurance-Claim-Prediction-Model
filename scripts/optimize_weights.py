import sys, joblib
from pathlib import Path
import numpy as np
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

sys.path.append('.')
from src.validation import normalized_gini
from src.config import load_config
from src.data_loader import load_data, split_data
from sklearn.isotonic import IsotonicRegression

config = load_config()
output_dir = Path('outputs')

print("Loading validation data...")
train_df, _ = load_data(config['data']['train_path'])
_, X_val_raw, _, y_val = split_data(train_df, config['features']['target'])

print("Applying preprocessing pipeline...")
feat_eng = joblib.load(output_dir / 'feat_eng.joblib')
imputer  = joblib.load(output_dir / 'imputer.joblib')
encoder  = joblib.load(output_dir / 'encoder.joblib')
selector = joblib.load(output_dir / 'selector.joblib')

X_val = selector.transform(
    encoder.transform(
        imputer.transform(
            feat_eng.transform(X_val_raw)
        )
    )
)

print("Generating predictions from saved models...")
models = {
    'LightGBM': joblib.load(output_dir / 'lightgbm_model.joblib'),
    'XGBoost':  joblib.load(output_dir / 'xgboost_model.joblib'),
    'CatBoost': joblib.load(output_dir / 'catboost_model.joblib'),
}
val_preds = {k: m.predict_proba(X_val)[:, 1] for k, m in models.items()}

def objective(trial):
    w_lgb = trial.suggest_float('w_lgb', 0.0, 1.0)
    w_xgb = trial.suggest_float('w_xgb', 0.0, 1.0)
    w_cat = trial.suggest_float('w_cat', 0.0, 1.0)
    total = w_lgb + w_xgb + w_cat
    if total == 0:
        return 0
    preds = (
        w_lgb * val_preds['LightGBM'] +
        w_xgb * val_preds['XGBoost'] +
        w_cat * val_preds['CatBoost']
    ) / total
    calibrator = IsotonicRegression(out_of_bounds='clip')
    calibrator.fit(preds, y_val)
    cal_preds = calibrator.transform(preds)
    return normalized_gini(y_val, cal_preds)

print("Running Optuna (200 trials) to find best ensemble weights...")
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=200)

best = study.best_trial.params
total = best['w_lgb'] + best['w_xgb'] + best['w_cat']
w_lgb = best['w_lgb'] / total
w_xgb = best['w_xgb'] / total
w_cat = best['w_cat'] / total

print("=" * 50)
print(f"Best Calibrated Gini: {study.best_value:.4f}")
print(f"LightGBM weight: {w_lgb:.4f}")
print(f"XGBoost  weight: {w_xgb:.4f}")
print(f"CatBoost weight: {w_cat:.4f}")
print("=" * 50)
