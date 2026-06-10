import sys
from pathlib import Path
import joblib
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.ensemble import generate_ensemble_predictions

def main():
    print("="*60)
    print("ZEBRA INFERENCE SCRIPT")
    print("="*60)
    
    config = load_config()
    test_path = project_root / config['data']['test_path']
    output_dir = project_root / config['data']['output_dir']
    
    if not test_path.exists():
        print(f"Error: Test data not found at {test_path}")
        return
        
    print(f"Loading test data from {test_path}...")
    if test_path.suffix == '.csv':
        test_df = pd.read_csv(test_path)
    else:
        test_df = pd.read_excel(test_path)
        
    # Extract IDs for submission
    ids = test_df['id']
    X_test = test_df.drop(columns=['id'])
    
    # Load Preprocessor
    preprocessor_path = output_dir / 'preprocessor.joblib'
    if not preprocessor_path.exists():
        print("Error: Preprocessor not found. Run scripts/train.py first.")
        return
        
    print("Loading preprocessor and transforming data...")
    preprocessor = joblib.load(preprocessor_path)
    X_test_proc = preprocessor.transform(X_test)
    
    # Load Models and Predict
    print("Loading models and generating predictions...")
    model_names = ['LightGBM', 'XGBoost', 'CatBoost']
    predictions = {}
    
    for name in model_names:
        model_path = output_dir / f"{name.lower()}_model.joblib"
        if model_path.exists():
            model = joblib.load(model_path)
            predictions[name] = model.predict_proba(X_test_proc)[:, 1]
        else:
            print(f"Warning: {name} model not found. Skipping.")
            
    if not predictions:
        print("Error: No models were found to generate predictions.")
        return
        
    # Generate Ensemble
    raw_weights = config['model']['ensemble_weights']
    weights = {
        'LightGBM': raw_weights.get('lightgbm', 0.1231),
        'XGBoost': raw_weights.get('xgboost', 0.2778),
        'CatBoost': raw_weights.get('catboost', 0.5991)
    }
    
    # Filter weights for only the models we successfully loaded
    active_weights = {k: v for k, v in weights.items() if k in predictions}
    weight_sum = sum(active_weights.values())
    active_weights = {k: v / weight_sum for k, v in active_weights.items()} # Normalize
    
    final_preds = generate_ensemble_predictions(predictions, active_weights)
    
    # Create submission file
    submission = pd.DataFrame({
        'id': ids,
        'target': final_preds
    })
    
    sub_path = output_dir / 'submission.csv'
    submission.to_csv(sub_path, index=False)
    
    print("\n" + "="*60)
    print(f"✅ Inference Complete! Submission saved to {sub_path}")
    print("="*60)

if __name__ == "__main__":
    main()
