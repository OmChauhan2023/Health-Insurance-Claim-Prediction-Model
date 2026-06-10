"""
ZEBRA Advanced Training Script - K-Fold CV + Rank Averaging + Calibration

Strategy:
1. 5-Fold Stratified Cross-Validation to generate Out-Of-Fold (OOF) predictions
2. OOF predictions used to calibrate final ensemble (no data leakage)
3. Final test predictions are averaged across all 5 folds per model
4. Rank averaging compared against weighted average, best one selected
5. Isotonic calibration on the best ensemble
"""
import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.isotonic import IsotonicRegression
from scipy.stats import rankdata

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraTargetEncoder, ZebraFeatureSelector, apply_resampling
from src.models import get_all_models
from src.validation import normalized_gini


def rank_average(predictions_dict):
    """Rank averaging — converts predictions to ranks then averages."""
    n = len(list(predictions_dict.values())[0])
    ranked = np.zeros(n)
    for preds in predictions_dict.values():
        ranked += rankdata(preds) / n
    return ranked / len(predictions_dict)


def main():
    print("=" * 80)
    print("ZEBRA ADVANCED TRAINING - 5-Fold CV + Rank Averaging + Calibration")
    print("=" * 80)

    config = load_config()
    train_path = project_root / config['data']['train_path']
    test_path  = project_root / config['data']['test_path']
    output_dir = project_root / config['data']['output_dir']
    output_dir.mkdir(exist_ok=True)

    target_col    = config['features']['target']
    random_state  = config['preprocessing']['random_state']
    n_folds       = 5

    # --- Load full training data ---
    print("\n--- [1] Loading Data ---")
    train_df, test_df = load_data(train_path, test_path)

    train_ids = train_df['id']
    y_all = train_df[target_col]
    X_all = train_df.drop(columns=[target_col, 'id'])

    test_ids = test_df['id']
    X_test_raw = test_df.drop(columns=['id'])

    print(f"Training samples: {len(X_all):,} | Test samples: {len(X_test_raw):,}")

    # --- Preprocessing (fit on all training data) ---
    print("\n--- [2] Full Preprocessing Pipeline ---")
    feat_eng = ZebraFeatureEngineer()
    X_all_eng  = feat_eng.fit_transform(X_all)
    X_test_eng = feat_eng.transform(X_test_raw)
    print(f"Features after engineering: {X_all_eng.shape[1]}")

    imputer = ZebraImputer(
        config['features']['binary'],
        config['features']['categorical'],
        config['features']['numeric']
    )
    X_all_imp  = imputer.fit_transform(X_all_eng)
    X_test_imp = imputer.transform(X_test_eng)

    encoder = ZebraTargetEncoder(config['features']['categorical'], smoothing=10)
    X_all_enc  = encoder.fit_transform(X_all_imp, y_all)
    X_test_enc = encoder.transform(X_test_imp)

    # Feature selection on all data
    selector = ZebraFeatureSelector(n_features=80, random_state=random_state)
    selector.fit(X_all_enc, y_all)
    X_all_sel  = selector.transform(X_all_enc)
    X_test_sel = selector.transform(X_test_enc)

    # Save preprocessing artifacts
    joblib.dump(feat_eng,  output_dir / 'feat_eng.joblib')
    joblib.dump(imputer,   output_dir / 'imputer.joblib')
    joblib.dump(encoder,   output_dir / 'encoder.joblib')
    joblib.dump(selector,  output_dir / 'selector.joblib')

    # --- 5-Fold Cross Validation ---
    print(f"\n--- [3] {n_folds}-Fold Stratified Cross-Validation ---")
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    model_names = ['LightGBM', 'XGBoost', 'CatBoost']

    # Containers
    oof_preds   = {name: np.zeros(len(X_all_sel)) for name in model_names}
    test_preds  = {name: np.zeros(len(X_test_sel)) for name in model_names}

    X_all_arr = X_all_sel.values if hasattr(X_all_sel, 'values') else X_all_sel
    y_all_arr = y_all.values

    for fold, (train_idx, val_idx) in enumerate(skf.split(X_all_arr, y_all_arr), 1):
        print(f"\n  --- Fold {fold}/{n_folds} ---")
        X_tr, X_val = X_all_arr[train_idx], X_all_arr[val_idx]
        y_tr, y_val = y_all_arr[train_idx], y_all_arr[val_idx]

        # Resample only the training fold
        X_tr_res, y_tr_res = apply_resampling(
            X_tr, y_tr,
            smote_ratio=config['preprocessing']['smote_ratio'],
            under_ratio=config['preprocessing']['under_ratio'],
            random_state=random_state
        )

        fold_models = get_all_models(random_state=random_state)

        for name, model in fold_models.items():
            print(f"  Training {name}...")
            if name == 'CatBoost':
                from sklearn.model_selection import train_test_split
                X_t, X_e, y_t, y_e = train_test_split(X_tr_res, y_tr_res, test_size=0.1, random_state=random_state)
                model.fit(X_t, y_t, eval_set=(X_e, y_e))
            else:
                model.fit(X_tr_res, y_tr_res)

            oof_preds[name][val_idx] = model.predict_proba(X_val)[:, 1]
            test_preds[name] += model.predict_proba(X_test_sel)[:, 1] / n_folds

        # Fold Gini scores
        for name in model_names:
            fold_gini = normalized_gini(y_val, oof_preds[name][val_idx])
            print(f"    {name}: Fold {fold} Gini = {fold_gini:.4f}")

    # --- OOF Evaluation ---
    print("\n--- [4] Full OOF Evaluation ---")
    for name in model_names:
        g = normalized_gini(y_all_arr, oof_preds[name])
        a = roc_auc_score(y_all_arr, oof_preds[name])
        print(f"{name:10} | OOF Gini: {g:.4f} | AUC: {a:.4f}")

    # --- Ensemble Comparison ---
    print("\n--- [5] Ensemble Comparison ---")
    weights = config['model']['ensemble_weights']
    w = {
        'LightGBM': weights.get('lightgbm', 0.281),
        'XGBoost':  weights.get('xgboost',  0.539),
        'CatBoost': weights.get('catboost',  0.180),
    }

    # Weighted average
    weighted_oof = sum(oof_preds[n] * w[n] for n in model_names)
    weighted_test = sum(test_preds[n] * w[n] for n in model_names)
    w_gini = normalized_gini(y_all_arr, weighted_oof)
    print(f"Weighted Avg OOF Gini : {w_gini:.4f}")

    # Rank average
    ranked_oof  = rank_average(oof_preds)
    ranked_test = rank_average(test_preds)
    r_gini = normalized_gini(y_all_arr, ranked_oof)
    print(f"Rank Avg  OOF Gini   : {r_gini:.4f}")

    # Pick best
    if r_gini >= w_gini:
        best_oof  = ranked_oof
        best_test = ranked_test
        print(">> Using Rank Averaging")
    else:
        best_oof  = weighted_oof
        best_test = weighted_test
        print(">> Using Weighted Averaging")

    # --- Isotonic Calibration on OOF ---
    print("\n--- [6] Isotonic Calibration ---")
    calibrator = IsotonicRegression(out_of_bounds='clip')
    calibrator.fit(best_oof, y_all_arr)
    cal_oof  = calibrator.transform(best_oof)
    cal_test = calibrator.transform(best_test)

    final_gini = normalized_gini(y_all_arr, cal_oof)
    final_auc  = roc_auc_score(y_all_arr, cal_oof)
    print("-" * 50)
    print(f"FINAL OOF Gini (calibrated): {final_gini:.4f} | AUC: {final_auc:.4f}")
    print("-" * 50)

    # --- Save Submission ---
    joblib.dump(calibrator, output_dir / 'calibrator.joblib')

    submission = pd.DataFrame({'id': test_ids, target_col: cal_test})
    sub_path = output_dir / 'submission_kfold.csv'
    submission.to_csv(sub_path, index=False)
    print(f"\nSubmission saved to {sub_path}")
    print("Training complete!")


if __name__ == "__main__":
    main()
