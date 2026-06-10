import sys
import os
from pathlib import Path

# Add project root to python path so we can import src
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import pandas as pd
from src.config import load_config
from src.visualization import (
    plot_target_distribution,
    plot_correlation_heatmap,
    plot_numeric_distributions
)

def main():
    print("="*60)
    print("ZEBRA Automated EDA Script")
    print("="*60)
    
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return
        
    train_path = project_root / config['data']['train_path']
    plots_dir = project_root / config['data']['plots_dir']
    
    # Ensure plots directory exists
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print(f"\nLoading training data from: {train_path}")
    if not train_path.exists():
        print(f"Error: Data file not found at {train_path}")
        return
        
    try:
        # Load CSV (if it's an excel file, you might need pd.read_excel)
        if train_path.suffix == '.csv':
            df = pd.read_csv(train_path)
        else:
            df = pd.read_excel(train_path)
        print(f"Data loaded successfully! Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
        
    target_col = config['features']['target']
    numeric_cols = config['features']['numeric']
    
    # 1. Plot Target Distribution
    print("\nGenerating Target Distribution Plot...")
    if target_col in df.columns:
        plot_target_distribution(
            df, 
            target_col, 
            output_path=str(plots_dir / 'target_distribution.png')
        )
        print(f"   Saved to {plots_dir / 'target_distribution.png'}")
    else:
        print(f"   Target column '{target_col}' not found.")
        
    # 2. Plot Numeric Distributions
    print("\nGenerating Numeric Distributions Plot...")
    available_numeric = [c for c in numeric_cols if c in df.columns]
    if available_numeric:
        plot_numeric_distributions(
            df,
            available_numeric,
            output_path=str(plots_dir / 'numeric_distributions.png')
        )
        print(f"   Saved to {plots_dir / 'numeric_distributions.png'}")
    else:
        print("   No numeric columns found.")
        
    # 3. Plot Correlation Heatmap
    print("\nGenerating Correlation Heatmap...")
    if available_numeric:
        # Take a subset of numeric features for the heatmap + target
        heatmap_features = available_numeric[:15]
        if target_col in df.columns and target_col not in heatmap_features:
            heatmap_features.append(target_col)
            
        plot_correlation_heatmap(
            df,
            heatmap_features,
            output_path=str(plots_dir / 'correlation_heatmap.png')
        )
        print(f"   Saved to {plots_dir / 'correlation_heatmap.png'}")
        
    print("\n" + "="*60)
    print(f"Automated EDA completed! All plots saved to: {plots_dir}")
    print("="*60)

if __name__ == "__main__":
    main()
