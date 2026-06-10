import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier

def get_lightgbm_model(random_state=42):
    # Optuna-tuned parameters — Val Gini: 0.2826
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt',
        'num_leaves': 27,
        'learning_rate': 0.030296,
        'n_estimators': 727,
        'max_depth': 6,
        'min_child_samples': 70,
        'reg_alpha': 1.968,
        'reg_lambda': 0.377,
        'feature_fraction': 0.529,
        'bagging_fraction': 0.708,
        'bagging_freq': 6,
        'min_gain_to_split': 0.267,
        'random_state': random_state,
        'verbose': -1
    }
    return lgb.LGBMClassifier(**params)

def get_xgboost_model(random_state=42):
    # Optuna-tuned parameters — Val Gini: 0.2824
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 6,
        'learning_rate': 0.0128,
        'n_estimators': 834,
        'subsample': 0.540,
        'colsample_bytree': 0.701,
        'min_child_weight': 10,
        'reg_alpha': 0.580,
        'reg_lambda': 2.606,
        'gamma': 0.248,
        'random_state': random_state,
        'tree_method': 'hist'
    }
    return xgb.XGBClassifier(**params)

def get_catboost_model(random_state=42):
    # Optuna-tuned parameters — Val Gini: 0.2848
    params = {
        'iterations': 1339,
        'learning_rate': 0.0103,
        'depth': 8,
        'l2_leaf_reg': 6.043,
        'border_count': 71,
        'random_seed': random_state,
        'verbose': False,
        'eval_metric': 'AUC',
        'early_stopping_rounds': 50
    }
    return CatBoostClassifier(**params)

def get_all_models(random_state=42):
    return {
        'LightGBM': get_lightgbm_model(random_state),
        'XGBoost': get_xgboost_model(random_state),
        'CatBoost': get_catboost_model(random_state)
    }
