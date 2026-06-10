import sys
from pathlib import Path
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data, split_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraCategoricalEncoder, apply_resampling
from src.models import get_all_models
from src.validation import normalized_gini
from src.ensemble import generate_ensemble_predictions

def main():
    print("="*80)
    print("ZEBRA ML PIPELINE - TRAINING SCRIPT")
    print("="*80)
    
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
    X_train_raw, X_val_raw, y_train, y_val = split_data(train_df, target_col, random_state=random_state)
    
    # 3. Preprocessing Pipeline
    print("\n--- [2] Preprocessing ---")
    preprocessor = Pipeline([
        ('feat_eng', ZebraFeatureEngineer()),
        ('imputer', ZebraImputer(
            config['features']['binary'],
            config['features']['categorical'],
            config['features']['numeric']
        )),
        ('encoder', ZebraCategoricalEncoder(config['features']['categorical']))
    ])
    
    print("Fitting preprocessor on training data...")
    X_train_processed = preprocessor.fit_transform(X_train_raw)
    
    print("Transforming validation data...")
    X_val_processed = preprocessor.transform(X_val_raw)
    
    # Save preprocessor
    joblib.dump(preprocessor, output_dir / 'preprocessor.joblib')
    print("Saved preprocessor to outputs/preprocessor.joblib")
    
    # 4. Resampling
    print("\n--- [3] Resampling Training Data ---")
    X_train_res, y_train_res = apply_resampling(
        X_train_processed, 
        y_train,
        smote_ratio=config['preprocessing']['smote_ratio'],
        under_ratio=config['preprocessing']['under_ratio'],
        random_state=random_state
    )
    
    # 5. Model Training
    print("\n--- [4] Model Training ---")
    models = get_all_models(random_state=random_state)
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_res, y_train_res)
        joblib.dump(model, output_dir / f'{name.lower()}_model.joblib')
        
    # 6. Evaluation
    print("\n--- [5] Evaluation ---")
    val_predictions = {}
    
    for name, model in models.items():
        preds = model.predict_proba(X_val_processed)[:, 1]
        val_predictions[name] = preds
        
        gini = normalized_gini(y_val, preds)
        auc = roc_auc_score(y_val, preds)
        print(f"{name:10} | Gini: {gini:.4f} | AUC: {auc:.4f}")
        
    # Ensemble Evaluation
    print("\nEvaluating Ensemble...")
    # Map weights to capitalize keys (from yaml) to match model names
    raw_weights = config['model']['ensemble_weights']
    weights = {
        'LightGBM': raw_weights.get('lightgbm', 0.1231),
        'XGBoost': raw_weights.get('xgboost', 0.2778),
        'CatBoost': raw_weights.get('catboost', 0.5991)
    }
    
    ensemble_preds = generate_ensemble_predictions(val_predictions, weights)
    ens_gini = normalized_gini(y_val, ensemble_preds)
    ens_auc = roc_auc_score(y_val, ensemble_preds)
    
    print("-" * 50)
    print(f"ENSEMBLE   | Gini: {ens_gini:.4f} | AUC: {ens_auc:.4f}")
    print("-" * 50)
    
    print(f"\n✅ Training complete! All artifacts saved to {output_dir}")

if __name__ == "__main__":
    main()
