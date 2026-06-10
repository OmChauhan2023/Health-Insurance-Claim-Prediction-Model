import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

def load_data(train_path: str, test_path: str = None) -> tuple:
    """
    Loads the training and (optionally) test datasets.
    """
    train_file = Path(train_path)
    
    if not train_file.exists():
        raise FileNotFoundError(f"Training data not found at {train_file.absolute()}")
        
    print(f"Loading training data from {train_file.name}...")
    if train_file.suffix == '.csv':
        train_df = pd.read_csv(train_file)
    else:
        train_df = pd.read_excel(train_file)
        
    test_df = None
    if test_path:
        test_file = Path(test_path)
        if test_file.exists():
            print(f"Loading test data from {test_file.name}...")
            if test_file.suffix == '.csv':
                test_df = pd.read_csv(test_file)
            else:
                test_df = pd.read_excel(test_file)
                
    return train_df, test_df

def split_data(df: pd.DataFrame, target_col: str, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    Splits the dataframe into training and validation sets, maintaining class distribution.
    """
    X = df.drop(columns=[target_col])
    if 'id' in X.columns:
        X = X.drop(columns=['id'])
        
    y = df[target_col]
    
    print(f"Splitting data with test_size={test_size} (Stratified)")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=y
    )
    
    return X_train, X_val, y_train, y_val
