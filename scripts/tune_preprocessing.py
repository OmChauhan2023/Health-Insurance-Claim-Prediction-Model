import sys
import itertools
from pathlib import Path
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

def main():
    print("=" * 60)
    print("PHASE 1: Preprocessing Grid Search")
    print("=" * 60)

    config = load_config()
    train_path = project_root / config['data']['train_path']
    target_col = config['features']['target']
    random_state = config['preprocessing']['random_state']

    print("\n[1] Loading Data...")
    train_df, _ = load_data(train_path)
    X_train_raw, X_val_raw, y_train, y_val = split_data(train_df, target_col, test_size=0.2, random_state=random_state)

    print("[2] Global Feature Engineering...")
    feat_eng = ZebraFeatureEngineer()
    X_train_eng = feat_eng.fit_transform(X_train_raw)
    X_val_eng = feat_eng.transform(X_val_raw)

    print("[3] Imputing...")
    imputer = ZebraImputer(config['features']['binary'], config['features']['categorical'], config['features']['numeric'])
    X_train_imp = imputer.fit_transform(X_train_eng)
    X_val_imp = imputer.transform(X_val_eng)

    print("[4] Target Encoding...")
    encoder = ZebraTargetEncoder(config['features']['categorical'], smoothing=10)
    X_train_enc = encoder.fit_transform(X_train_imp, y_train)
    X_val_enc = encoder.transform(X_val_imp)

    # Grid Search Parameters
    percentiles = [0.52, 0.55, 0.57, 0.60, 0.62, 0.65, 0.67, 0.70, 0.72, 0.75]
    smote_ratios = [0.05]  # Locked to grid search winner
    under_ratios = [0.3]   # Locked to grid search winner

    best_score = 0
    best_params = {}

    print("\n[5] Starting Grid Search (High Percentiles)...")
    # Cache resampling to save time
    for s_ratio in smote_ratios:
        for u_ratio in under_ratios:
            print(f"\n>> Resampling: SMOTE={s_ratio}, Under={u_ratio}")
            X_train_res, y_train_res = apply_resampling(X_train_enc, y_train, smote_ratio=s_ratio, under_ratio=u_ratio, random_state=random_state)
            
            for p in percentiles:
                # Fast Feature Selection
                selector = ZebraFeatureSelector(keep_percentile=p, random_state=random_state)
                X_train_sel = selector.fit_transform(X_train_res, y_train_res)
                X_val_sel = selector.transform(X_val_enc)
                
                # Fast LightGBM eval model
                model = lgb.LGBMClassifier(n_estimators=100, max_depth=5, learning_rate=0.05, random_state=random_state, verbose=-1, n_jobs=-1)
                model.fit(X_train_sel, y_train_res)
                
                preds = model.predict_proba(X_val_sel)[:, 1]
                gini = normalized_gini(y_val, preds)
                
                print(f"     Percentile={p} | Features={X_train_sel.shape[1]} | Gini={gini:.5f}")
                
                if gini > best_score:
                    best_score = gini
                    best_params = {
                        'keep_percentile': p,
                        'smote_ratio': s_ratio,
                        'under_ratio': u_ratio
                    }

    print("\n" + "=" * 60)
    print("BEST PREPROCESSING COMBINATION:")
    print(f"Gini Score: {best_score:.5f}")
    print(best_params)
    print("=" * 60)

if __name__ == "__main__":
    main()
