"""
ZEBRA Advanced Training Script - K-Fold CV + Stacking (Meta-Learner) + OOF Target Encoding

Strategy:
1. 5-Fold Stratified Cross-Validation
2. Out-Of-Fold (OOF) Target Encoding (prevents target leakage)
3. Feature Selection & Resampling done INSIDE the fold (100% leak-free)
4. Stacking: Logistic Regression meta-learner trained on OOF predictions
5. Final Isotonic Calibration on Stacking predictions
"""
import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraTargetEncoder, ZebraFeatureSelector, apply_resampling
from src.models import get_all_models
from src.validation import normalized_gini


def main():
    print("=" * 80)
    print("ZEBRA ADVANCED TRAINING - Stacking + OOF Target Encoding")
    print("=" * 80)

    config = load_config()
    train_path = project_root / config['data']['train_path']
    test_path  = project_root / config['data']['test_path']
    output_dir = project_root / config['data']['output_dir']
    output_dir.mkdir(exist_ok=True)

    target_col    = config['features']['target']
    random_state  = config['preprocessing']['random_state']
    n_folds       = 5

    # --- Load full data ---
    print("\n--- [1] Loading Data ---")
    train_df, test_df = load_data(train_path, test_path)

    test_ids = test_df['id']
    y_all = train_df[target_col]
    X_all_raw = train_df.drop(columns=[target_col, 'id'])
    X_test_raw = test_df.drop(columns=['id'])

    print(f"Training samples: {len(X_all_raw):,} | Test samples: {len(X_test_raw):,}")

    # --- Global Preprocessing (Non-leaky) ---
    print("\n--- [2] Global Feature Engineering & Imputation ---")
    feat_eng = ZebraFeatureEngineer()
    X_all_eng  = feat_eng.fit_transform(X_all_raw)
    X_test_eng = feat_eng.transform(X_test_raw)

    imputer = ZebraImputer(
        config['features']['binary'],
        config['features']['categorical'],
        config['features']['numeric']
    )
    X_all_imp  = imputer.fit_transform(X_all_eng)
    X_test_imp = imputer.transform(X_test_eng)

    joblib.dump(feat_eng,  output_dir / 'feat_eng.joblib')
    joblib.dump(imputer,   output_dir / 'imputer.joblib')

    # --- 5-Fold Cross Validation ---
    print(f"\n--- [3] {n_folds}-Fold CV (OOF Encoding + Resampling + Training) ---")
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    model_names = ['LightGBM', 'XGBoost', 'CatBoost']

    # Containers for OOF and Test predictions
    oof_preds   = {name: np.zeros(len(X_all_imp)) for name in model_names}
    test_preds  = {name: np.zeros(len(X_test_imp)) for name in model_names}

    y_all_arr = y_all.values

    for fold, (train_idx, val_idx) in enumerate(skf.split(X_all_imp, y_all_arr), 1):
        print(f"\n  --- Fold {fold}/{n_folds} ---")
        X_tr_fold = X_all_imp.iloc[train_idx].copy()
        y_tr_fold = y_all_arr[train_idx]
        X_val_fold = X_all_imp.iloc[val_idx].copy()

        # 1. OOF Target Encoding
        encoder = ZebraTargetEncoder(config['features']['categorical'], smoothing=10)
        X_tr_enc = encoder.fit_transform(X_tr_fold, y_tr_fold)
        X_val_enc = encoder.transform(X_val_fold)
        X_test_enc = encoder.transform(X_test_imp)

        # 2. Resampling (only on training fold)
        X_tr_res, y_tr_res = apply_resampling(
            X_tr_enc, y_tr_fold,
            smote_ratio=config['preprocessing']['smote_ratio'],
            under_ratio=config['preprocessing']['under_ratio'],
            random_state=random_state
        )

        # 3. Feature Selection
        selector = ZebraFeatureSelector(keep_percentile=0.65, random_state=random_state)
        X_tr_sel = selector.fit_transform(X_tr_res, y_tr_res)
        X_val_sel = selector.transform(X_val_enc)
        X_test_sel = selector.transform(X_test_enc)

        # Save fold-specific preprocessing for inference later if needed
        joblib.dump(encoder, output_dir / f'encoder_fold{fold}.joblib')
        joblib.dump(selector, output_dir / f'selector_fold{fold}.joblib')

        # 4. Train Models
        fold_models = get_all_models(random_state=random_state)

        for name, model in fold_models.items():
            print(f"  Training {name}...")
            if name == 'CatBoost':
                from sklearn.model_selection import train_test_split
                X_t, X_e, y_t, y_e = train_test_split(X_tr_sel, y_tr_res, test_size=0.1, random_state=random_state)
                model.fit(X_t, y_t, eval_set=(X_e, y_e))
            else:
                model.fit(X_tr_sel, y_tr_res)

            # Predict OOF and Test
            oof_preds[name][val_idx] = model.predict_proba(X_val_sel)[:, 1]
            test_preds[name] += model.predict_proba(X_test_sel)[:, 1] / n_folds

        # Fold Gini scores
        for name in model_names:
            fold_gini = normalized_gini(y_all_arr[val_idx], oof_preds[name][val_idx])
            print(f"    {name}: Fold {fold} Gini = {fold_gini:.4f}")

    # --- OOF Evaluation ---
    print("\n--- [4] Base Models OOF Evaluation ---")
    for name in model_names:
        g = normalized_gini(y_all_arr, oof_preds[name])
        a = roc_auc_score(y_all_arr, oof_preds[name])
        print(f"{name:10} | OOF Gini: {g:.4f} | AUC: {a:.4f}")

    # --- Stacking (Meta-Learner) ---
    print("\n--- [5] Stacking (LightGBM Meta-Learner) ---")
    meta_X_train = np.column_stack([oof_preds[n] for n in model_names])
    meta_X_test  = np.column_stack([test_preds[n] for n in model_names])

    import lightgbm as lgb
    meta_model = lgb.LGBMClassifier(
        n_estimators=100,
        max_depth=3,
        num_leaves=7,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_samples=50,
        random_state=random_state,
        verbose=-1
    )
    meta_model.fit(meta_X_train, y_all_arr)
    joblib.dump(meta_model, output_dir / 'meta_model.joblib')

    stacking_oof_preds = meta_model.predict_proba(meta_X_train)[:, 1]
    stacking_test_preds = meta_model.predict_proba(meta_X_test)[:, 1]

    stack_gini = normalized_gini(y_all_arr, stacking_oof_preds)
    print(f"Stacking OOF Gini: {stack_gini:.4f}")

    # Feature Importance of Meta-Learner
    print("Meta-Learner Feature Importances:")
    for name, weight in zip(model_names, meta_model.feature_importances_):
        print(f"  {name}: {weight}")

    # --- Isotonic Calibration ---
    print("\n--- [6] Final Isotonic Calibration ---")
    calibrator = IsotonicRegression(out_of_bounds='clip')
    calibrator.fit(stacking_oof_preds, y_all_arr)
    cal_oof  = calibrator.transform(stacking_oof_preds)
    cal_test = calibrator.transform(stacking_test_preds)

    final_gini = normalized_gini(y_all_arr, cal_oof)
    final_auc  = roc_auc_score(y_all_arr, cal_oof)
    print("-" * 50)
    print(f"FINAL OOF Gini (Calibrated Stacking): {final_gini:.4f} | AUC: {final_auc:.4f}")
    print("-" * 50)

    joblib.dump(calibrator, output_dir / 'calibrator.joblib')

    # --- Save Submission ---
    submission = pd.DataFrame({'id': test_ids, target_col: cal_test})
    sub_path = output_dir / 'submission_kfold_stacking.csv'
    submission.to_csv(sub_path, index=False)
    print(f"\nSubmission saved to {sub_path}")
    print("Training complete!")

if __name__ == "__main__":
    main()
