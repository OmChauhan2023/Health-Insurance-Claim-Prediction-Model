import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set global aesthetic parameters for better visuals
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def plot_target_distribution(df: pd.DataFrame, target_col: str, output_path: str = None):
    """Plots the distribution of the target variable (Count and Percentage)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Count plot
    counts = df[target_col].value_counts()
    counts.plot(kind='bar', ax=axes[0], color=['#2ecc71', '#e74c3c'])
    axes[0].set_title('Target Distribution (Count)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Target Class')
    axes[0].set_ylabel('Count')
    axes[0].set_xticklabels(['No Claim (0)', 'Claim (1)'], rotation=0)
    
    # Percentage plot
    pct = df[target_col].value_counts(normalize=True) * 100
    pct.plot(kind='bar', ax=axes[1], color=['#2ecc71', '#e74c3c'])
    axes[1].set_title('Target Distribution (Percentage)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Target Class')
    axes[1].set_ylabel('Percentage (%)')
    axes[1].set_xticklabels(['No Claim (0)', 'Claim (1)'], rotation=0)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_correlation_heatmap(df: pd.DataFrame, features: list, output_path: str = None):
    """Plots a correlation heatmap for a subset of features."""
    plt.figure(figsize=(14, 12))
    corr_matrix = df[features].corr()
    
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_numeric_distributions(df: pd.DataFrame, numeric_features: list, output_path: str = None):
    """Plots histograms for up to 9 numeric features."""
    sample_features = numeric_features[:9]
    n_features = len(sample_features)
    
    if n_features == 0:
        return
        
    rows = (n_features + 2) // 3
    fig, axes = plt.subplots(rows, min(n_features, 3), figsize=(15, 4 * rows))
    if n_features > 1:
        axes = axes.flatten()
    else:
        axes = [axes]
        
    for idx, feat in enumerate(sample_features):
        sns.histplot(df[feat], bins=30, ax=axes[idx], color='skyblue', edgecolor='black', alpha=0.7, kde=True)
        axes[idx].set_title(f'Distribution of {feat}', fontsize=10, fontweight='bold')
        axes[idx].set_xlabel('Value')
        axes[idx].set_ylabel('Frequency')
        
        # Add statistics lines
        mean_val = df[feat].mean()
        median_val = df[feat].median()
        axes[idx].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
        axes[idx].axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
        axes[idx].legend(fontsize=8)
        
    # Hide any unused axes
    for idx in range(n_features, len(axes)):
        fig.delaxes(axes[idx])
        
    plt.suptitle('Numeric Features Distribution Overview', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
