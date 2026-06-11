import sys
from pathlib import Path
import pandas as pd
import lightgbm as lgb

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.config import load_config
from src.data_loader import load_data
from src.feature_engineering import ZebraFeatureEngineer
from src.preprocessing import ZebraImputer, ZebraTargetEncoder, apply_resampling

def main():
    print("Loading data...")
    config = load_config()
    train_path = project_root / config['data']['train_path']
    train_df, _ = load_data(train_path)
    
    target_col = config['features']['target']
    random_state = config['preprocessing']['random_state']
    
    y = train_df[target_col]
    X = train_df.drop(columns=[target_col, 'id'])
    
    print("Feature Engineering...")
    eng = ZebraFeatureEngineer()
    X_eng = eng.fit_transform(X)
    
    print("Imputing...")
    imputer = ZebraImputer(
        config['features']['binary'],
        config['features']['categorical'],
        config['features']['numeric']
    )
    X_imp = imputer.fit_transform(X_eng)
    
    print("Target Encoding...")
    encoder = ZebraTargetEncoder(config['features']['categorical'], smoothing=10)
    X_enc = encoder.fit_transform(X_imp, y)
    
    print("Resampling...")
    X_res, y_res = apply_resampling(
        X_enc, y,
        smote_ratio=config['preprocessing']['smote_ratio'],
        under_ratio=config['preprocessing']['under_ratio'],
        random_state=random_state
    )
    
    print("Training LightGBM Feature Selector...")
    model = lgb.LGBMClassifier(n_estimators=100, random_state=random_state, verbose=-1)
    model.fit(X_res, y_res)
    
    importance = pd.DataFrame({
        'Feature': X_res.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    output_path = project_root / 'outputs' / 'feature_importances.csv'
    output_path.parent.mkdir(exist_ok=True)
    importance.to_csv(output_path, index=False)
    
    print(f"Feature importance saved to: {output_path}")
    print("\nTop 20 Features:")
    print(importance.head(20).to_string(index=False))
    print("\nBottom 20 Features:")
    print(importance.tail(20).to_string(index=False))

if __name__ == "__main__":
    main()
