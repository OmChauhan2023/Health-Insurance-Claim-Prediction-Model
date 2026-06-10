import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score
from sklearn.isotonic import IsotonicRegression
from sklearn.model_selection import train_test_split

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data, split_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import (
    ZebraImputer,
    ZebraTargetEncoder,
    ZebraFeatureSelector,
    apply_resampling
)
from src.models import get_all_models
from src.validation import normalized_gini
from src.ensemble import generate_ensemble_predictions


def main():
    print("=" * 80)
    print("ZEBRA ML PIPELINE - TRAINING SCRIPT v2 (Target Encoding + Calibration)")
    print("=" * 80)

    # 1. Setup & Config
    config = load_config()
    train_path = project_root / config['data']['train_path']
    output_dir = project_root / config['data']['output_dir']
    output_dir.mkdir(exist_ok=True)

    target_col = config['features']['target']
    random_state = config['preprocessing']['random_state']

    # 2. Data Loading
    print("\n--- [1] Loading Data ---")
    train_df, _ = load_data(train_path)
    X_train_raw, X_val_raw, y_train, y_val = split_data(
        train_df, target_col, random_state=random_state
    )

    # 3. Feature Engineering
    print("\n--- [2] Feature Engineering ---")
    feat_eng = ZebraFeatureEngineer()
    X_train_eng = feat_eng.fit_transform(X_train_raw)
    X_val_eng = feat_eng.transform(X_val_raw)
    print(f"Features after engineering: {X_train_eng.shape[1]}")

    # 4. Imputation (fit on train only)
    print("\n--- [3] Imputation ---")
    imputer = ZebraImputer(
        config['features']['binary'],
        config['features']['categorical'],
        config['features']['numeric']
    )
    X_train_imp = imputer.fit_transform(X_train_eng)
    X_val_imp = imputer.transform(X_val_eng)

    # 5. Target Encoding (fit on train only, using y_train)
    print("\n--- [4] Target Encoding (smoothing=10) ---")
    encoder = ZebraTargetEncoder(
        categorical_features=config['features']['categorical'],
        smoothing=10
    )
    X_train_enc = encoder.fit_transform(X_train_imp, y_train)
    X_val_enc = encoder.transform(X_val_imp)
    print(f"Target encoding applied to {len(config['features']['categorical'])} categorical features.")

    # Save preprocessing objects
    joblib.dump(feat_eng, output_dir / 'feat_eng.joblib')
    joblib.dump(imputer, output_dir / 'imputer.joblib')
    joblib.dump(encoder, output_dir / 'encoder.joblib')

    # 6. Resampling (only on training data)
    print("\n--- [5] Resampling Training Data ---")
    X_train_res, y_train_res = apply_resampling(
        X_train_enc, y_train,
        smote_ratio=config['preprocessing']['smote_ratio'],
        under_ratio=config['preprocessing']['under_ratio'],
        random_state=random_state
    )

    # 7. Feature Selection (top 80)
    print("\n--- [6] Feature Selection (top 80) ---")
    selector = ZebraFeatureSelector(n_features=80, random_state=random_state)
    X_train_sel = selector.fit_transform(X_train_res, y_train_res)
    X_val_sel = selector.transform(X_val_enc)
    joblib.dump(selector, output_dir / 'selector.joblib')

    # 8. Model Training
    print("\n--- [7] Model Training ---")
    models = get_all_models(random_state=random_state)
    val_predictions = {}

    for name, model in models.items():
        print(f"Training {name}...")
        if name == 'CatBoost':
            # CatBoost needs a small eval set for early stopping
            X_tr, X_es, y_tr, y_es = train_test_split(
                X_train_sel, y_train_res, test_size=0.1, random_state=random_state
            )
            model.fit(X_tr, y_tr, eval_set=(X_es, y_es))
        else:
            model.fit(X_train_sel, y_train_res)

        joblib.dump(model, output_dir / f'{name.lower()}_model.joblib')
        val_predictions[name] = model.predict_proba(X_val_sel)[:, 1]

    # 9. Evaluation (before calibration)
    print("\n--- [8] Evaluation ---")
    raw_weights = config['model']['ensemble_weights']
    weights = {
        'LightGBM': raw_weights.get('lightgbm', 0.1231),
        'XGBoost':  raw_weights.get('xgboost', 0.2778),
        'CatBoost': raw_weights.get('catboost', 0.5991)
    }

    for name, preds in val_predictions.items():
        print(f"{name:10} | Gini: {normalized_gini(y_val, preds):.4f} | AUC: {roc_auc_score(y_val, preds):.4f}")

    ensemble_preds = generate_ensemble_predictions(val_predictions, weights)
    ens_gini = normalized_gini(y_val, ensemble_preds)
    ens_auc  = roc_auc_score(y_val, ensemble_preds)
    print("-" * 50)
    print(f"ENSEMBLE   | Gini: {ens_gini:.4f} | AUC: {ens_auc:.4f}  (before calibration)")

    # 10. Isotonic Calibration
    print("\n--- [9] Isotonic Calibration ---")
    calibrator = IsotonicRegression(out_of_bounds='clip')
    calibrator.fit(ensemble_preds, y_val)
    calibrated_preds = calibrator.transform(ensemble_preds)

    cal_gini = normalized_gini(y_val, calibrated_preds)
    cal_auc  = roc_auc_score(y_val, calibrated_preds)
    print("-" * 50)
    print(f"ENSEMBLE   | Gini: {cal_gini:.4f} | AUC: {cal_auc:.4f}  (after calibration)")
    print("-" * 50)

    joblib.dump(calibrator, output_dir / 'calibrator.joblib')
    joblib.dump(weights, output_dir / 'ensemble_weights.joblib')

    print(f"\nTraining complete! All artifacts saved to {output_dir}")


if __name__ == "__main__":
    main()
