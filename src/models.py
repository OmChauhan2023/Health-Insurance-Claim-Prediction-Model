import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier

def get_lightgbm_model(random_state=42):
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'max_depth': 7,
        'min_child_samples': 20,
        'reg_alpha': 0.1,
        'reg_lambda': 0.1,
        'random_state': random_state,
        'n_estimators': 500,
        'verbose': -1
    }
    return lgb.LGBMClassifier(**params)

def get_xgboost_model(random_state=42):
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'max_depth': 6,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 3,
        'reg_alpha': 0.1,
        'reg_lambda': 1,
        'random_state': random_state,
        'n_estimators': 500
    }
    return xgb.XGBClassifier(**params)

def get_catboost_model(random_state=42):
    params = {
        'iterations': 500,
        'learning_rate': 0.05,
        'depth': 6,
        'l2_leaf_reg': 3,
        'random_seed': random_state,
        'verbose': False,
        'eval_metric': 'AUC'
    }
    return CatBoostClassifier(**params)

def get_all_models(random_state=42):
    return {
        'LightGBM': get_lightgbm_model(random_state),
        'XGBoost': get_xgboost_model(random_state),
        'CatBoost': get_catboost_model(random_state)
    }
